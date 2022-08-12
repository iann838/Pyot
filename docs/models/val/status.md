# Status 

Module: `pyot.models.val.status` 

### _class_ `Status`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `platform`: `str = models.val.DEFAULT_PLATFORM` 

Endpoints: 
* `status_v1_platform_data`: `[]` 

Attributes: 
* `id` -> `str` 
* `name` -> `str` 
* `locales` -> `List[str]` 
* `maintenances` -> `List[pyot.models.val.status.StatusDetailData]` 
* `incidents` -> `List[pyot.models.val.status.StatusDetailData]` 


### _class_ `StatusContentData`

Type: `PyotStatic` 

Attributes: 
* `locale` -> `str` 
* `content` -> `str` 


### _class_ `StatusDetailData`

Type: `PyotStatic` 

Attributes: 
* `id` -> `int` 
* `maintenance_status` -> `str` 
* `incident_severity` -> `str` 
* `titles` -> `List[pyot.models.val.status.StatusContentData]` 
* `updates` -> `List[pyot.models.val.status.StatusUpdateData]` 
* `created_at_strftime` -> `str` 
* `archive_at_strftime` -> `str` 
* `updated_at_strftime` -> `str` 
* `platforms` -> `List[str]` 

Properties: 
* _property_ `archive_at` -> `datetime.datetime` 
* _property_ `created_at` -> `datetime.datetime` 
* _property_ `updated_at` -> `datetime.datetime` 


### _class_ `StatusUpdateData`

Type: `PyotStatic` 

Attributes: 
* `id` -> `int` 
* `author` -> `str` 
* `publish` -> `bool` 
* `publish_locations` -> `List[str]` 
* `translations` -> `List[pyot.models.val.status.StatusContentData]` 
* `created_at_strftime` -> `str` 
* `updated_at_strftime` -> `str` 

Properties: 
* _property_ `created_at` -> `datetime.datetime` 
* _property_ `updated_at` -> `datetime.datetime` 


