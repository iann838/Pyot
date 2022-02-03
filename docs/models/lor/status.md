# Status 

Module: `pyot.models.lor.status` 

### _class_ Status

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `region`: `str = models.lor.DEFAULT_REGION` 

Endpoints: 
* `status_v1_platform_data`: `[]` 

Attributes: 
* `id` -> `str` 
* `name` -> `str` 
* `locales` -> `List[str]` 
* `maintenances` -> `List[pyot.models.lor.status.StatusDetailData]` 
* `incidents` -> `List[pyot.models.lor.status.StatusDetailData]` 

Properties: 
* _property_ `region` -> `str` 


### _class_ StatusContentData

Type: `PyotStatic` 

Attributes: 
* `locale` -> `str` 
* `content` -> `str` 


### _class_ StatusDetailData

Type: `PyotStatic` 

Attributes: 
* `id` -> `int` 
* `maintenance_status` -> `str` 
* `incident_severity` -> `str` 
* `created_at_strftime` -> `str` 
* `updated_at_strftime` -> `str` 
* `archive_at_strftime` -> `str` 
* `titles` -> `List[pyot.models.lor.status.StatusContentData]` 
* `updates` -> `List[pyot.models.lor.status.StatusUpdateData]` 
* `platforms` -> `List[str]` 

Properties: 
* _property_ `archive_at` -> `datetime.datetime` 
* _property_ `created_at` -> `datetime.datetime` 
* _property_ `updated_at` -> `datetime.datetime` 


### _class_ StatusUpdateData

Type: `PyotStatic` 

Attributes: 
* `id` -> `int` 
* `author` -> `str` 
* `publish` -> `bool` 
* `publish_locations` -> `List[str]` 
* `created_at_strftime` -> `str` 
* `updated_at_strftime` -> `str` 
* `translations` -> `List[pyot.models.lor.status.StatusContentData]` 

Properties: 
* _property_ `created_at` -> `datetime.datetime` 
* _property_ `updated_at` -> `datetime.datetime` 


