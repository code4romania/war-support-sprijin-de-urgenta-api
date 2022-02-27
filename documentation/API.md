# API Documentation
**Table of contents:**

* [Add Resource](#add_resource)
* [Search](#search)
* [Update Resource](#update_resource)
* [Get all categories](#get_all_categories)
* [Get all subcategories of category](#get_all_subcategories_of_category)
* [Get all donor types](#get_all_donor_types)

This API could be extended in the future with

##  <a name="add_resource" id="add_resource">Add Resource</a>
Method: **POST**

Header:   “Authorization”: "Basic <login_token>"

Base-URL: /add-resource


### _Example of request:_
```
{
    "name": "example",
    "description": "",
    "expiration_date": "15-09-2022",
    "sub_category": 1,
    "donor_name": "",
    "donor_contact_name": "",
    "donor_email": "",
    "donor_phone_number": "",
    "donor_county": "",
    "donor_details": {},
    "donor_type": 0
}
```
Required fields:
* name | description | category | donor_name | donor_email | donor_type

Data types:
```
    "name": str,
    "description": str,
    "expiration_date": str,  # %d-%m-%Y
    "sub_category": int,
    "donor_name": str,
    "donor_contact_name": str,
    "donor_email": str,
    "donor_phone_number": str,
    "donor_county": str,
    "donor_details": JSON,
    "donor_type": int  # choices= [0,1,2,3]
```

Donor types
```
    INDIVIDUAL = 0
    COMPANY = 1
    PUBLIC_BODY = 2
    NON_PROFIT = 3
```

### _Success response:_
```
HTTP Status Code: 200
 {
    "success": true,
}
```

### _Generic error response:_
```
HTTP Status Code: 400
{
  "success": false,
  "error": "BAD REQUEST"
}
```


## <a name="search" id="search">Search</a>
Method: **GET**

Base-URL: /search/?{field1}={some value}&{field2}={some value}

List of fields that we can use in our search:
name, sub_category, donor_name, donor_contact_name, donor_email,
donor_phone_number, donor_county, donor_type.

OBS: this request will only return available resources and that have expiration
date still valid.

Pagination: the search GET request will return a list of maximum 100 resource 
objects. To see the next page you should request it by adding `?page={int}`

### _Example of request:_
```
curl {Base_URL}/search/?sub_category=2&name=example?page=2
```

### _Success response:_
```
HTTP Status Code: 200
[
   {
    "id": 123,
    "name": "example",
    "description": "",
    "expiration_date": "15-09-2022",
    "sub_category": 2,
    "donor_name": "",
    "donor_contact_name": "",
    "donor_email": "",
    "donor_phone_number": "",
    "donor_county": "",
    "donor_details": {},
    "donor_type": 0
    },
       {
    "id": 123,
    "name": "example",
    "description": "",
    "expiration_date": "15-09-2022",
    "sub_category": 2,
    "donor_name": "",
    "donor_contact_name": "",
    "donor_email": "",
    "donor_phone_number": "",
    "donor_county": "",
    "donor_details": {},
    "donor_type": 0
    }
]
```

## <a name="update_resource" id="update_resource">Update Resource</a>
Method: **POST**

Header:   “Authorization”: "Basic <login_token>"

Base-URL: /update_resource/pk={int}/


OBS: Minimum one field is required (ex: we can use this request to mark a resource
as `available= false`)
### _Example of request:_
```
{
    "name": "example",
    "description": "",
    "expiration_date": "15-09-2022",
    "available": false,
    "sub_category": 1,
    "donor_name": "",
    "donor_contact_name": "",
    "donor_email": "",
    "donor_phone_number": "",
    "donor_county": "",
    "donor_details": {},
    "donor_type": 0
}
```
### _Success response:_
```
HTTP Status Code: 200
 {
    "success": true,
}
```


## <a name="get_all_categories" id="get_all_categories">Get all categories</a>
Method: **GET**
Base-URL: /get-categories/

### _Success response:_
```
[
    {
        "id": 1,
        "name": "example"
    },
    {
        "id": 2,
        "name": "example"
    }
]
```

## <a name="get_all_subcategories_of_category" id="get_all_subcategories_of_category">Get all subcategories of category</a>
Method: **GET**

Base-URL: /get-subcategories/

### _Success response:_
```
[
    {
        "id": 1,
        "name": "example"
    },
    {
        "id": 2,
        "name": "example"
    }
]
```

## <a name="get_all_donor_types" id="get_all_donor_types">Get all donor types</a>
Method: **GET**

Base-URL: /get-donor-types/

### _Success response:_
```
[
    {
        "id": 1,
        "name": "example"
    },
    {
        "id": 2,
        "name": "example"
    }
]
```