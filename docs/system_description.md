Sprijin De Urgenta - a humanitarian aid system meant to help connect victims with volunteers and government authorities in order to effectively delver aid to them in a coordinated and verified manner.

Users of this system:
1. Victim (private person)
2. Donor (private person / private company / gov. official / govmt)
3. Volunteer (gov. official / private person)
4. Admin (gov. official)

Roles of Users:
* Victim: requests and receives aid
* Donor: offers goods or services, performs services. Can be a person or a company.
* Volunteer: offers goods or services, performs services, performs privileged services (i.e. verifiying validity of stock, services)
* Admin: manages goods, services, requests for aid, volunteers, service assignment, userbase, verifies (or delegates) validity of stock

Minimum Data requirements per user type:
* Victim: Name, Surname, Nationality, Gender, Date of Birth, Location (address+gps), contact_details
* Donor_Person: Name, Surname, CNP, contact_details
* Donor_company: Name, CUI, contact_details, points_of_contact (users registered within the system)
* Volunteer: Name, Surname, contact_detials, CNP
* Admin: Name, Surname, CNP, contact_details

Resources in the system:
* Goods - can be given directly to Victims
  * Comsumable Goods
    * Food
    * Drinks
    * Medicine
    * Hygene products
    * etc.
  * Non Consumable, Non Reusable Goods 
    * Clothes
    * Tooth Brushes
    * Sim Cards
    * Shavers
    * Devices (i.e. phones, radios, etc)
    * etc. 
  * Non Consumable, Reusable Products (reuse is not mandatory)
    * Blankets 
    * Pillows
    * etc.
* Services - can be offered to users by users
    * Translation
    * Transport
    * Hosting
    * Storage
    * Counseling
    * Medical
    * Cooking
* Support Resources - can't be given directly to victims, these support service offering and volunteers
    * Locations (with facilities, connect with owner & points of contact)
        * Storage
        * Hosting
    * Vehicles (connects with driver)
    
When a user offers a service, depending on what service it is, more data may need to be collected about the user and the support resources required.
An example of this would be the following scenario:
Andrei has registered with the platform to be a volunteer and distribute blankets.
He then wishes to transport some of the victims using his personal car to a nearby town. 
He already has an account on the platform, so he just needs to offer the people transportation service.
When he does that, the system asks him for his driver's license number and details about his vehicle.
i.e. driver_id, vehicle_id (reg plate), capacity (nr seats), facilities (accepts_pets, etc)
Refer to the data model to see how this would be represented.


Resource requirements
Important requirement is that due to the shifting nature of this operations (things changing constantly, mistakes being made, etc):
1. Admins must be able to modify, delete, add any of the above entities into the system via DJAdmin
2. Admins must be able to get a clear picture of the status of offers-request matchings (in order to be able to easily confirm / update the status)
3. Corrections done by admins via DJAdmin directly in the database must not impact the correct operation of the backend services.
i.e. relevant events must be fired by JDAdmin, caches must be invalidated if need be, backend matching and other operations must use the source of truth (which will be directly edited by DJADmin)
4. DJAdmin should be used mainly to update / input new data into the system rather than perform operations. Matching requests with offers, finding information about users and assigning them aid should be done via a backend service.

Use cases:
Victim:
- as a victim, i request aid (requesting a set of resources) [any number of times]
- as a victim, i can see the status of my aid requests
- as a victim, i can close a request as not needed anymore or received

Donor:
- as a donor, i offer goods to the relief effort.
- as a donor, i can view/edit my goods offers.
- as a donor, i can remove my goods offers.
- as a donor, i can see the reserved resources (quantity and type) and who to give them to.
- as a donor, i can signal goods have been given away to a volunteer or directly to a victim

- as a donor, i offer services to the relief effort (create offer)
- as a donor, i can update the status of my offered services. (update offer status)
- as a donor, i can remove my offered services.

Volunteer:
- as a volunteer, i can request goods to distribute
- as a volunteer, i can mark goods given to me as distributed

- as a volunteer, i can offer to perform services. (additional data may be collected here, i.e. driver's license, vehicle details and facilities)
- as a volunteer, i can update the status of my offered services (in progress, unavailable, free, etc)
- as a volunteer, i can remove my offered services

- as a volunteer, i can see requests for a service i'm offering ordered by distance from me.
- as a volunteer, i can offer to carry out a request for a service i'm providing
- as a volunteer, i can mark a request as completed (here the admins can then verify with receiver, and close)
  ---- maybe a bit later on --------------------
- as a volunteer, i can request supporting_resources to use
- as a volunteer, i can change the status of supporting_resources received
- as a volunteer, i can free supporting resources given to me

Admin:
- as an admin, i can add victims into the system directly
- as an admin, i can view all the victims from the system
- as an admin, i can filter / search for victims by certain fields (name, nationality, location)
- as an admin, i can add resources into the system directly
- as an admin, i can view all the resources from the system
- as an admin, i can filter / search for resources by cretain fields (type, sub_type, location, availability, status)
- as an admin, i can view victim requests
- as an admin, i can filter / search for victim requests by fields (type, sub_type, location, submit_time)
- as an admin, i can confim a victim request (i.e. change its status)
- as an admin, i can close a victim request
- as an admin, i can insert a victim request directly into the system
- as an admin, i can auto resolve a victim request using the system. The system will find the closest resources requested by the victim, and as an admin I can verify each one and reserve it.
- as an admin, i can reserve a certain quantity of resources form a given location (reserve mening it will be set aside for someone to act on them)

System requirements:
1. The system must be resistent to data loss. [Resilience]
    - periodic backups should be performet and set to S3 (or other storage solution) - must-have
      The backup should be in a format that the database supports and can restore from.
2. A history of all performed operations should be kept [Audit & Accontability]
    - the backend systems must fire events in a queue each time an operation is performed. These events are consumed and stored (either file or S3) in an ordered by timestamp log.
      (recommended format: schema on read - so that the loc can be analysed with 3rd party tools easily in case analysis needs to be performed later)

Execution Flows:
//ToDo.
