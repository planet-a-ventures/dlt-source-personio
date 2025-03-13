{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

let
  spec_folder = "dlt_source_personio/model/spec";
in
{
  packages = [
    pkgs.git
    pkgs.bash
    pkgs.python312Packages.openapi-spec-validator
  ];

  languages.python.enable = true;
  languages.python.uv.enable = true;
  languages.python.uv.package = pkgs.uv;
  languages.python.uv.sync.enable = true;
  languages.python.uv.sync.allExtras = true;
  languages.python.venv.enable = true;
  languages.python.version = "3.12";

  scripts.generate-model.exec = ''
    ./dlt_source_personio/model/generate_model.sh
  '';

  scripts.validate-spec.exec = ''
    openapi-spec-validator \
      --schema 3.1.0 \
      --errors all \
      dlt_source_personio/model/v2_spec/*.yaml
  '';

  scripts.update-spec.exec = ''
    GIT_MERGE_AUTOEDIT=no \
      git subtree pull \
      --prefix ${spec_folder} \
      https://github.com/personio/api-docs.git \
      master \
      --squash
  '';

  scripts.refresh-model.exec = ''
    set -euo pipefail
    update-spec
    generate-model
    git add dlt_source_personio/model/spec.py
    git commit -m'chore: update model'
  '';

  git-hooks.hooks = {
    shellcheck.enable = true;
    black.enable = true;
    typos.enable = true;
    typos.excludes = [
      spec_folder
      "dlt_source_personio/model/v1"
    ];
    yamllint.enable = true;
    yamlfmt.enable = true;
    yamlfmt.settings.lint-only = false;
    check-toml.enable = true;
    commitizen.enable = true;
    nixfmt-rfc-style.enable = true;
    mdformat.enable = true;
    mdformat.excludes = [
      spec_folder
    ];
    mdformat.package = pkgs.mdformat.withPlugins (
      ps: with ps; [
        mdformat-frontmatter
      ]
    );
    markdownlint.enable = true;
    autoflake.enable = true;
  };

  scripts.format.exec = ''
    yamlfmt .
    markdownlint --fix .
    pre-commit run --all-files
  '';

  scripts.test-all.exec = ''
    pytest -s -vv "$@"
  '';

  enterTest = ''
    validate-spec
    test-all
  '';

  scripts.build.exec = ''
    uv build
  '';

  scripts.sample-pipeline-run.exec = ''
    python personio_pipeline.py
  '';

  scripts.sample-pipeline-show.exec = ''
    dlt pipeline personio_pipeline show
  '';
}
