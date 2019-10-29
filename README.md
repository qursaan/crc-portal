# CRC Federation Portal 
The purpose of federation is to establish the interconnection between two or more independent testbeds for creating a richer testing environment, which increase the experimentation multilateral benefits rather than the users of the individual testbeds. The portal allows researchers to access through out different testbed. The goal of federation portal is to simplify the large-scale of testbed web access and management over different infrastructure and organization.

## Architecture
### Design
The following list are main design description for testbed federation system:
* **Site independence**: each site must running based on its own information and resources without need of any external services.
* **Authorization Hierarchy**: the authorization level is used to inherit all permission from parent site. So, each site has a higher privilege to change and update its resources information or change the reservation plan.
* **Resource sharing**: While the site is running the federation system, each site can setup the details of resources and its sharing plan.
* **Sharing permission**: The administrator must approve the request of sharing per site to accept the site resources.
* **Resources Synchronization**: As well as, site is running independently, the site is responsible for distributing the entries information to other registered sites. And other sites is responsible for collecting all resources information from registered
sites. 

![Federation system architecture design including testbed portal.](/help/credit_arch.png)*Federation system architecture design including testbed portal.*


