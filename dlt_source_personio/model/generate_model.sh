#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

log() {
    >&2 echo "$@"
}

codegen() {
    log "  Running codegen with args: $*"

    datamodel-codegen \
        --input-file-type yaml \
        --output-model-type pydantic_v2.BaseModel \
        --use-annotated \
        --use-union-operator \
        --use-subclass-enum \
        --capitalise-enum-members \
        --use-field-description \
        --input-file-type openapi \
        --field-constraints \
        --use-double-quotes \
        --use-pendulum \
        --additional-imports "pydantic_extra_types.pendulum_dt.Date,pydantic_extra_types.pendulum_dt.DateTime" \
        --disable-timestamp \
        "$@"
}

main() {
    pushd "${SCRIPT_DIR}" >/dev/null

    local python_version
    python_version=$(./current_python_major_minor.py)

    log "Current Python version: ${python_version}"

    local file
    local b
    local second_segment
    local second_segment_capitalized

    log ""
    log "V1 spec"

    for file in spec/personio-*.yaml; do
        b=$(basename "${file}" .yaml)
        second_segment=$(echo "${b}" | cut -d'-' -f2)
        second_segment_capitalized="${second_segment^}"

        log "• Processing file: ${file}"
        codegen \
            --target-python-version "${python_version}" \
            --input "${file}" \
            --output "v1/${second_segment}.py" \
            --base-class "..v1.My${second_segment_capitalized}BaseModel"

    done

    log ""
    log "V2 spec"

    local basename_capitalized
    for file in v2_spec/*.yaml; do
        b=$(basename "${file}" .yaml)
        basename_capitalized="${b^}"

        log "• Processing file: ${file}"
        codegen \
            --target-python-version "${python_version}" \
            --input "${file}" \
            --output "v2/${b}.py" \
            --base-class "..v2.My${basename_capitalized}BaseModel"
    done    

    log ""
    log "✔ Generated code"

    popd >/dev/null
}

main "$@"
