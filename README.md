Some stuff

### Endpoints

base url: https://difoxy2.pythonanywhere.com

#### Login

| Endpoint                         | Usage                                                                     | Role			required<br />(Authorization:			Bearer {token}) |
| -------------------------------- | ------------------------------------------------------------------------- | :----------------------------------------------------: |
| /auth/users<br />`POST`        | Creates			a new user account<br />`body {username, email and password}` |                           --                           |
| /auth/users/me/<br />`GET`     | Displays			current user details                                           |                 Any			valid user token                 |
| /auth/token/login/<br />`POST` | Retrieve			access tokens for user<br />`body {username, password}`      |                           --                           |



#### Business Logic

| Endpoint                                                    | Usage                                                                                                  | Role			required <br />(Authorization:			Bearer {token} |
| -------------------------------- | ------------------------------------------------------------------------- | :----------------------------------------------------: |
| /api/menu-items<br />`GET`<br />`option query string: ` | Lists			all menu items                                                                                 | --                                                     |
| /api/menu-items/{menuItemId}<br />`GET`                   | Lists			single menu item                                                                               | --                                                     |
| /api/menu-items<br />`POST`                               | Creates			a new menu item<br />`body {title, price, category_id}`                                    | Admin			or Manager                                     |
| /api/menu-items/{menuItemId}<br />`PUT` `PATCH`         | Updates			single menu item<br />`body {title, price, category_id}`                                   | Admin			or Manager                                     |
| /api/menu-items/{menuItemId}<br />`DELETE`                | Deletes			menu item                                                                                    | Admin			or Manager                                     |
| /api/cart/menu-items<br />`GET`                           | Returns			items in cart for current user                                                               | Customer                                               |
| /api/cart/menu-items<br />`POST`                          | Adds			the menu itemsto			cart of			current user<br /> `body {menuitem_id, quantity}`                | Customer                                               |
| /api/cart/menu-items<br />`DELETE`                        | Empty			cartof			current user                                                                          | Customer                                               |
| /api/orders<br />`GET`                                    | Returns			all orders created by current user                                                           | Customer                                               |
| /api/orders<br />`GET`                                    | Returns			all orderswith			“delivery_crew” field =			current delivery crew                           | Delivery			crew                                        |
| /api/orders<br />`GET`                                    | Returns			all orders of all users                                                                      | Admin			or Manager                                     |
| /api/orders<br />`POST`                                   | Creates			a new order from current			cart items, will remove all items in cart                         | Customer                                               |
| /api/orders/{orderId}<br />`GET`                          | Returns			all items for this order id.                                                                 | Customer			who created the order                       |
| /api/orders/{orderId}<br />`PATCH`                        | Update			“delivery_crew”			or “status”			field of this order<br />`body {delivery_crew, status}` | Manager                                                |
| /api/orders/{orderId}<br />`PATCH`                        | Update			“status”			field of this order<br />`body {delivery_crew, status}`                        | Delivery			crewassigned			to this order                |
| /api/orders/{orderId}<br />`DELETE`                       | Delete			order                                                                                         | Manager                                                |



#### User Role Management

| Endpoint                                                 | Usage                                                                             | Role			required <br />(Authorization:			Bearer {token}) |
| -------------------------------- | ------------------------------------------------------------------------- | :----------------------------------------------------: |
| /api/groups/manager/users<br />`GET`                   | Returns			all managers                                                            | Admin			or Manager                                      |
| /api/groups/manager/users<br />`POST`                  | Assigns			the user in the payload to the manager group<br />`body {username}`   | Admin			or Manager                                      |
| /api/groups/manager/users/{userId}<br />`DELETE`       | Removes			manager			from manager role                                             | Admin			or Manager                                      |
| /api/groups/delivery-crew/users<br />`GET`             | Returns			all delivery crew                                                       | Admin			or Manager                                      |
| /api/groups/delivery-crew/users<br />`POST`            | Assigns			the user in the payload to delivery crew group<br />`body {username}` | Admin			or Manager                                      |
| /api/groups/delivery-crew/users/{userId}<br />`DELETE` | Removes			this userId from the delivery-cres group                                | Admin			or Manager                                      |


Some other stuff
