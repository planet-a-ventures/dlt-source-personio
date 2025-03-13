# generated by datamodel-codegen:
#   filename:  personio-recruiting-api.yaml

from __future__ import annotations

from enum import Enum
from typing import Annotated, Any, Dict, List
from uuid import UUID

from pendulum import Date
from pydantic import EmailStr, Field, RootModel
from pydantic_extra_types.pendulum_dt import Date, DateTime

from ..v1 import MyRecruitingBaseModel


class Type(str, Enum):
    SYSTEM = "system"
    CUSTOM = "custom"


class Phase(MyRecruitingBaseModel):
    type: Type
    """
    The type of application phase.
    """
    id: str | int
    """
    For custom phases this is an integer. The IDs for your custom phases can be found under your personio settings (https://{YOUR_COMPANY}.personio.de/configuration/recruiting/phases).

    For system phases this is a string and must be one of:
    - unassigned
    - rejected
    - withdrawn
    - offer
    - accepted
    """


class Category(str, Enum):
    CV = "cv"
    COVER_LETTER = "cover-letter"
    EMPLOYMENT_REFERENCE = "employment-reference"
    CERTIFICATE = "certificate"
    WORK_SAMPLE = "work-sample"
    OTHER = "other"


class File(MyRecruitingBaseModel):
    uuid: UUID
    """
    Reference to a previously uploaded file. Use the `uuid` value returned from the documents endpoint here.
    """
    original_filename: str
    category: Category
    """
    Category of referenced document.
    """


class Attribute(MyRecruitingBaseModel):
    id: str
    """
    Ids for custom attributes have the form `custom_attribute_123` and can be found can be found in your personio settings as `API name` when expanding the details of each attribute (https://{YOUR_COMPANY}.personio.de/configuration/recruiting/attributes).

    Ids for supported system attributes are:
    - birthday (YYYY-MM-DD)
    - gender (male / female / diverse / undefined)
    - location
    - phone
    - available_from
    - salary_expectations
    """
    value: str
    """
    Value of the attribute.

    For OPTION attributes, this must be one of the predefined options.

    For DATE attributes, this needs to follow ISO 8601 Local date, i.e. `2021-04-30`
    """


class SubmitApplication(MyRecruitingBaseModel):
    first_name: Annotated[str, Field(min_length=1)]
    """
    First name(s) of the applicant. Must not be empty or only whitespaces
    """
    last_name: Annotated[str, Field(min_length=1)]
    """
    Last name(s) of the applicant. Must not be empty or only whitespaces.
    """
    email: EmailStr
    """
    Email address of the applicant.
    """
    job_position_id: int
    """
    The personio internal id of the job this application should belong to.
    """
    recruiting_channel_id: int | None = None
    """
    The recruiting channel this application was sourced from.

    See https://{YOUR_COMPANY}.personio.de/configuration/recruiting/channels
    """
    external_posting_id: str | None = None
    """
    The external id of the job posting (E.g. the external id forwarded by Gohiring).
    """
    message: str | None = None
    """
    The applicant supplied free-text message.
    """
    application_date: Date | None = None
    """
    The application date (yyyy-mm-dd). It cannot be a date in the future.
    """
    phase: Phase | None = None
    """
    This can be a system or a custom application phase. When not provided, the application will be created with the initial phase according to the configuration for this job position's category (https://{YOUR_COMPANY}.personio.de/configuration/recruiting/categories).

    When an invalid phase is provided (e.g. a non-existent custom phase or one that is not configured for this job position's category), the application will be created with the phase `unassigned`.
    """
    tags: List[str] | None = None
    """
    Tags to be associated with this application. Non-existing tags will be created.

    See https://{YOUR_COMPANY}.personio.de/configuration/recruiting/tags
    """
    files: List[File] | None = None
    """
    References to previously uploaded files. These will be attached to the new application.

    Each file item consists of a `uuid`, an `original_filename` and a `category` (To see exact description, click on "ADD OBJECT").
    """
    attributes: List[Attribute] | None = None
    """
    Attributes for this applicant.

    Each attribute item consists of an `id` and a `value` (To see exact description, click on "ADD OBJECT").
    """


class Extension(str, Enum):
    PDF = "pdf"
    PPTX = "pptx"
    XLSX = "xlsx"
    DOCX = "docx"
    DOC = "doc"
    XLS = "xls"
    PTT = "ptt"
    ODS = "ods"
    ODT = "odt"
    FIELD_7Z = "7z"
    GZ = "gz"
    RAR = "rar"
    ZIP = "zip"
    BMP = "bmp"
    GIF = "gif"
    JPG = "jpg"
    PNG = "png"
    TIF = "tif"
    CSV = "csv"
    TXT = "txt"
    RTF = "rtf"
    MP4 = "mp4"
    FIELD_3GP = "3gp"
    MOV = "mov"
    AVI = "avi"
    WMV = "wmv"


class UploadedDocument(MyRecruitingBaseModel):
    uuid: UUID
    """
    The UUID of this file. Can be attached to an application by including this uuid in the application creation request.
    """
    size: int
    """
    Uploaded file size in bytes.
    """
    mimetype: str
    """
    Detected Mime Type of this file.
    """
    original_filename: str
    extension: Extension


class Error(MyRecruitingBaseModel):
    reason: str
    """
    An error code. See description.
    """
    context: Dict[str, Any] | None = None
    """
    Optional context on the error code.
    """


class Errors(MyRecruitingBaseModel):
    field: str
    """
    Indicates location of the error. Values are guaranteed to be unique in the `errors` array.
    """
    errors: List[Error]
    """
    All errors of this field.
    """


class Errors1(MyRecruitingBaseModel):
    id: UUID
    """
    Internal error reference.
    """
    status: str
    """
    HTTP status code
    """
    title: str
    """
    HTTP Status reason
    """
    detail: str | None = None


class ErrorResponse(MyRecruitingBaseModel):
    errors: List[Errors | Errors1]


class Response(MyRecruitingBaseModel):
    success: bool
    data: Dict[str, Any]


class EmploymentType(str, Enum):
    PERMANENT = "permanent"
    INTERN = "intern"
    TRAINEE = "trainee"
    FREELANCE = "freelance"


class Seniority(str, Enum):
    ENTRY_LEVEL = "entry-level"
    EXPERIENCED = "experienced"
    EXECUTIVE = "executive"
    STUDENT = "student"


class Schedule(str, Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


class YearsOfExperience(str, Enum):
    LT_1 = "lt-1"
    FIELD_1_2 = "1-2"
    FIELD_2_5 = "2-5"
    FIELD_5_7 = "5-7"
    FIELD_7_10 = "7-10"
    FIELD_10_15 = "10-15"
    GT_15 = "gt-15"


class JobDescription1(MyRecruitingBaseModel):
    name: str | None = None
    value: str | None = None


class JobDescription(MyRecruitingBaseModel):
    jobDescription: JobDescription1 | None = None


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    DIVERSE = "diverse"
    UNDEFINED = "undefined"


class Document(MyRecruitingBaseModel):
    file: bytes | None = None
    """
    allowed extensions are 'pdf', 'docx', 'doc', 'jpg', 'png', 'txt', 'jpeg', 'odt', 'ods','xlsx', 'rtf', 'xls', 'pptx', 'ppt', 'gif', 'tif', 'tiff', 'bmp', 'csv', 'rar', 'gz', 'zip', '7z' filesize per document < 20M total post size < 64M
    """


class JobDescriptionItem(RootModel[List[JobDescription]]):
    root: Annotated[
        List[JobDescription],
        Field(
            examples=[
                [
                    {
                        "name": "Beschreibung",
                        "value": '<![CDATA[ Für unser Büro mitten im Münchner Glockenbachviertel suchen wir zum nächstmöglichen Zeitpunkt einen Office Manager (m/w) in Teilzeit, der/ die sich um alle Themen rund ums Office zuverlässig kümmert.<br><br><strong>Deine Aufgaben:</strong><br><br><ul><li>Ansprechpartner in Sachen Büro, Ausstattung und anderer “Wohlfühl”-Themen, die unseren Mitarbeiter/innen auf dem Herzen liegen</li><li>Bearbeitung von generellen Anfragen, Post und Eingangsrechnungen</li><li>Kommunikation und Organisation unserer Servicedienstleister und Zulieferer</li><li>Selbstständige Entwicklung &amp; Umsetzung neuer Ideen, Aktionen und Events für unsere Mitarbeiter</li><li>Unterstützung unseres Management-Teams bei organisatorischen Aufgaben</li><li>Management unserer <strong><a href="https://www.unumotors.com">Unu-Elektroroller</a></strong>-Flotte (ja, du bekommst auch einen, wenn du möchtest)</li></ul> ]]>',
                    },
                    {
                        "name": "Dein Profil",
                        "value": "<![CDATA[ <ul><li>Du bist herzlich, offen und kommunikativ</li><li>Du bist ein Organisationstalent und magst den Umgang mit Zahlen</li><li>Du bist gewissenhaft, sorgfältig und strukturiert</li><li>Du zeigst Eigeninitiative und Kreativität bei der Planung neuer Aktionen</li><li>Du sprichst Deutsch auf muttersprachlichem Niveau und hast gute Englischkenntnisse</li><li>Du hast Spaß an vielfältigen Aufgaben und unterstützt gerne dort, wo Hilfe gebraucht wird</li></ul> ]]>",
                    },
                    {
                        "name": "Warum Personio",
                        "value": "<![CDATA[ <ul><li>Chance in einem schnell wachsenden Unternehmen an vielfältigen Aufgaben zu wachsen und zu lernen</li><li>Kreatives Arbeitsumfeld und kurze Entscheidungswege</li><li>Von Anfang an volle Verantwortung in Deinem Bereich</li><li>Regelmäßige Team-Events, Tischtennis und Ausflüge ins Münchner Nachtleben</li><li>Büro im Herzen von München (nahe Gärtnerplatz)</li><li>Blitzschneller Elektroroller deiner Wahl als “Geschäftswagen”</li></ul> ]]>",
                    },
                ]
            ]
        ),
    ]


class Applicant(MyRecruitingBaseModel):
    company_id: int
    """
    Your company ID (see endpoint description)
    """
    access_token: str
    """
    API Access token for your company account (see endpoint description)
    """
    job_position_id: int
    """
    ID of the published job position that this application is for (from XML feed)
    """
    first_name: Annotated[str, Field(max_length=255)]
    """
    First name of the applicant
    """
    last_name: Annotated[str, Field(max_length=255)]
    """
    Last name of the applicant
    """
    email: Annotated[str, Field(max_length=255)]
    """
    Email address of the applicant
    """
    gender: Gender | None = None
    """
    Gender of the applicant
    """
    recruiting_channel_id: int | None = None
    """
    ID of the recruiting channel that this applicant applied through recruiting_channel_id has to match the id of a channel you created in Personio
    """
    external_posting_id: Annotated[str | None, Field(max_length=255)] = None
    """
    When using multiposting, this is the `pid` forwarded (usually as a query param) by the external job board site
    """
    phone: Annotated[str | None, Field(max_length=255)] = None
    """
    Phone number of the applicant
    """
    location: Annotated[str | None, Field(max_length=255)] = None
    """
    Current location of the applicant
    """
    salary_expectations: Annotated[str | None, Field(max_length=255)] = None
    """
    Salary expectations of the applicant (Will not be parsed, so you can transfer values like "minimum 50k")
    """
    available_from: Annotated[str | None, Field(max_length=100)] = None
    """
    Date from which this applicant is available from
    """
    categorised_documents_n__file_: Annotated[
        bytes | None, Field(alias="categorised_documents[n][file]")
    ] = None
    """
    Nth document <br/> The file should be an upload stream. <br/> You can check a request example in the "A note on categorised documents" section. <br/> [array of files] <br/> allowed extensions are 'pdf', 'docx', 'doc', 'jpg', 'png', 'txt', 'jpeg', 'odt', 'ods','xlsx', 'rtf', 'xls', 'pptx', 'ppt', 'gif', 'tif', 'tiff', 'bmp', 'csv', 'rar', 'gz', 'zip', '7z'; <br/> filesize per document < 20M; <br/> total post size < 64M; <br/>
    """
    categorised_documents_n__category_: Annotated[
        str | None, Field(alias="categorised_documents[n][category]")
    ] = None
    """
    Nth document's category <br/> Category of the Nth file. <br/> You can check a request example in the "A note on categorised documents" section. <br/> allowed values are 'cv', 'cover-letter', 'employment-reference', 'certificate', 'work-sample' or 'other' <br/>
    """
    documents_n_: Annotated[bytes | None, Field(alias="documents[n]")] = None
    """
    Nth document <br/> The file should be an upload stream. <br/> allowed extensions are 'pdf', 'docx', 'doc', 'jpg', 'png', 'txt', 'jpeg', 'odt', 'ods','xlsx', 'rtf', 'xls', 'pptx', 'ppt', 'gif', 'tif', 'tiff', 'bmp', 'csv', 'rar', 'gz', 'zip', '7z'; <br/> filesize per document < 20M; <br/> total post size < 64M; <br/>
    """
    document_n_: Annotated[Document | None, Field(alias="document{n}")] = None
    """
    Alternatively to an array (see 'documents'), documents can also be transferred individually numbered document1, document2, etc (the numbering starts at 1) with the absolute path to the document in an upload stream. <br/> [file] <br/> allowed extensions are 'pdf', 'docx', 'doc', 'jpg', 'png', 'txt', 'jpeg', 'odt', 'ods','xlsx', 'rtf', 'xls', 'pptx', 'ppt', 'gif', 'tif', 'tiff', 'bmp', 'csv', 'rar', 'gz', 'zip', '7z'; <br/> filesize per document < 20M; <br/> total post size < 64M <br/>
    """
    message: str | None = None
    """
    Initial message from the applicant
    """
    tags: Any | None = None
    """
    Existing tags (new ones cannot be created via API) <br/> [array of strings], e.g. [ “tag_1”, “tag_2" ]
    """
    birthday: Date | None = None
    """
    Birthday of the applicant. <br/> Date according to ISO 8601 format (YYYY-MM-DD)
    """
    custom_attribute__id_: Annotated[
        int | None, Field(alias="custom_attribute_{id}")
    ] = None
    """
    Custom applicant attribute. <br/> Custom applicant attributes that were created individually can also be passed. <br/> You can find the unique parameter names of these attributes in your Personio account under: <pre>https://{YOUR_COMPANY}.personio.de/configuration/recruiting/applicants</pre>
    """


class JobDescriptions(MyRecruitingBaseModel):
    jobDescription: List[JobDescriptionItem] | None = None


class JobPosting(MyRecruitingBaseModel):
    id: Annotated[int | None, Field(examples=[4103])] = None
    subcompany: Annotated[str | None, Field(examples=[""])] = None
    office: Annotated[str | None, Field(examples=["Munich"])] = None
    department: Annotated[str | None, Field(examples=["Management"])] = None
    recruitingCategory: Annotated[Any | None, Field(examples=["Various"])] = None
    name: Annotated[
        Any | None, Field(examples=["Office- und Feelgood Manager (m/w)"])
    ] = None
    jobDescriptions: Annotated[
        JobDescriptions | None, Field(title="Job Descriptions")
    ] = None
    employmentType: Annotated[EmploymentType | None, Field(examples=["permanent"])] = (
        None
    )
    seniority: Annotated[Seniority | None, Field(examples=["entry-level"])] = None
    schedule: Annotated[Schedule | None, Field(examples=["full-time"])] = None
    yearsOfExperience: Annotated[YearsOfExperience | None, Field(examples=["lt-1"])] = (
        None
    )
    keywords: Annotated[
        str | None,
        Field(
            examples=[
                "office manager,project management,büro,assistenz,organisation,part time,Teilzeit"
            ]
        ),
    ] = None
    occupation: Annotated[Any | None, Field(examples=["office_management"])] = None
    occupationCategory: Annotated[
        Any | None, Field(examples=["administrative_and_clerical"])
    ] = None
    createdAt: Annotated[Any | None, Field(examples=["2016-05-31T12:14:07+0200"])] = (
        None
    )


class XmlResponse(MyRecruitingBaseModel):
    posting: List[JobPosting] | None = None
