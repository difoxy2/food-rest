Some stuff

### Endpoints

base url: https://difoxy2.pythonanywhere.com

#### Login

| Endpoint                         | Usage                                                                     | Role			required<br />(Authorization:			Bearer {token}) |
| -------------------------------- | ------------------------------------------------------------------------- | :----------------------------------------------------: |
| /auth/users<br />`POST`        | Creates			a new user account<br />`body {username, email and password}` |                           --                           |
| /auth/users/me/<br />GET         | Displays			current user details                                           |                 Any			valid user token                 |
| /auth/token/login/<br />`POST` | Retrieve			access tokens for user<br />`body {username, password}`      |                           --                           |



#### Business Logic

| Endpoint                                                                                                                        | Usage                                                                                              | Role			required (Authorization:			Bearer {token} |
| ------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| /api/menu-items<br />`GET`<br />`option query string: ?category=main&max_price=6&min_price=4&orderby=price&perpage=5&page2` | Lists			all menu items                                                                             | --                                               |
| /api/menu-items/{id}<br />`GET`                                                                                               | Lists			single menu item                                                                           | --                                               |
| POST			 /api/menu-items                                                                                                         | Creates			a new menu item body			{title, price, category_id}                                       | Admin			or Manager                               |
| PUT,			PATCH  /api/menu-items/{menuItem}                                                                                        | Updates			single menu item body			{title, price, category_id}                                      | Admin			or Manager                               |
| DELETE			/api/menu-items/{menuItem}                                                                                             | Deletes			menu item                                                                                | Admin			or Manager                               |
| GET			 /api/cart/menu-items                                                                                                     | Returns			items in cart for current user                                                           | Customer                                         |
| POST			 /api/cart/menu-items                                                                                                    | Adds			the menu itemsto			cartof			current user  body{menuitem_id,			quantity}                     | Customer                                         |
| DELETE			 /api/cart/menu-items                                                                                                  | Empty			cartof			current user                                                                      | Customer                                         |
| GET			 /api/orders``                                                                                                            | Returns			all orders created by current user                                                       | Customer                                         |
| GET			 /api/orders                                                                                                              | Returns			all orderswith			“delivery_crew” field=			current delivery crew                        | Delivery			crew                                  |
| GET			 /api/orders                                                                                                              | Returns			all orders of all users                                                                  | Admin			or Manager                               |
| POST			 /api/orders                                                                                                             | Creates			a new order from current			cart items, will remove all items in cart                     | Customer                                         |
| GET			 /api/orders/{orderId}                                                                                                    | Returns			all items for this order id.                                                             | Customer			who created the order                 |
| PATCH			 /api/orders/{orderId}``                                                                                                | Update			“delivery_crew”			or “status”			field of this order``  body			{delivery_crew, status} | Manager                                          |
| PATCH			 /api/orders/{orderId}``                                                                                                | Update			“status”			field of this order``  body			{delivery_crew, status}                        | Delivery			crewassigned			to this order          |
| DELETE			 /api/orders/{orderId}                                                                                                 | Delete			order                                                                                     | Manager                                          |



#### User Role Management

| Endpoint                                           | Usage                                                                                 | Role			required (Authorization:			Bearer {token}) |
| -------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------- |
| GET			 /api/groups/manager/users                   | Returns			all managers                                                                | Admin			or Manager                                |
| POST			 /api/groups/manager/users                  | Assigns			the user in the payload to the manager group``  body			{username}    | Admin			or Manager                                |
| DELETE			 /api/groups/manager/users/{userId}       | Removes			manager			from manager role                                                 | Admin			or Manager                                |
| GET			 /api/groups/delivery-crew/users             | Returns			all delivery crew                                                           | Admin			or Manager                                |
| POST			 /api/groups/delivery-crew/users``   | Assigns			the user in the payload to delivery crew group``   body			{username} | Admin			or Manager                                |
| DELETE			 /api/groups/delivery-crew/users/{userId} | Removes			this userId from the delivery-cres group                                    | Admin			or Manager                                |


Some other stuff
