# Market-Monitor

## Market Monitor Ideas

Users will be able to view certain stocks and track them in real-time. Each stock will be designated a category (Currency, Tech, etc.). Each stock category will have related category articles on the category page for those stocks referencing trends and world events that can impact that stock in the past/present/future. Users can use an investment simulator that will allow them to trade fake currency on real stock movement to view how simulated stocks would pay off. A history of past trades will be logged in this component.

### CRUD Features:

#### User Profile:
- **Create**: Users can sign up and create a new account on the application.
- **Read**: Users can view their profile page that will include a username, bio, and profile pic.
- **Update**: Users can edit their profile information listed above at any time.
- **Delete**: Users can delete their profile from the application at any time.

#### Watchlist Stocks/Pin articles (2):
- **Create**: Users can add stocks to their watchlist and pin articles to tabbed sections in their profile page.
- **Read**: Users can navigate to a watchlist/pinned stocks and articles sections to view the corresponding stocks and articles.
- **Delete**: Users can remove stocks/articles from the corresponding sections from their profile. (Add categories to move each stock/article into on these components for possible UPDATE functionality)

#### Planner/Notes sections (2):
**Notes**:
- **Create**: Users can add comments on stocks/articles to benchmark and track trends they are noticing to plan out trading intentions.
- **Read**: Users can view their notes on stock/article detail pages with dates on when the note was posted.
- **Update**: Users can edit their notes to add in additional information they receive as events/stocks progress.
- **Delete**: Users can delete their comments on both of these components at any time.

**Planner**:
- **Create**: Users can add daily, weekly, and monthly goals in a planning section of their user profile page.
- **Read**: Users can view their plans in each corresponding section on their profile page.
- **Update**: Users can edit these plans at any time from the profile page.
- **Delete**: Users can delete these plans at any time from the profile page.

### Bonus Feature:

#### Investment Simulator:
- **Create**: Users can create trades with fake currency based on real stock movement to see how potential trades will pan out.
- **Read**: Users can view the status of currently active trades on this page.
- **Update**: Users can cancel or edit buyout points at any time during an existing trade.
- **Delete**: Users can cancel active trades at any time and delete from trade history.

## Polygon API

- Might manage stock articles as well.
[https://polygon.io/stocks](https://polygon.io/stocks?utm_term=stock%20apis&utm_campaign=Stocks+-+USA&utm_source=adwords&utm_medium=ppc&hsa_acc=4299129556&hsa_cam=1330311037&hsa_grp=133850757326&hsa_ad=591207294226&hsa_src=g&hsa_tgt=kwd-437434011047&hsa_kw=stock%20apis&hsa_mt=e&hsa_net=adwords&hsa_ver=3&gad_source=1&gclid=CjwKCAiAivGuBhBEEiwAWiFmYT0z8lkcLm5dYhYmma4dd23k7WjMcPGAhkJFCH3RERmXcdXNz4LEDBoCycwQAvD_BwE)

## Chart.js

- Track active trades status in real time


![alt text](DB_Schema.png)

## API Documentation


### USER AUTHENTICATION/AUTHORIZATION


#### Endpoints requiring proper authorization

- **Require Authentication Response**:
  - **Status Code**: 401
  - **Body**:
    ```json
    {
      "message": "Authentication required"
    }
    ```

#### Endpoints requiring proper authorization

- **Require Proper Authorization Response**:
  - **Status Code**: 403
  - **Body**:
    ```json
    {
      "message": "Forbidden"
    }
    ```

#### User Signup

- **Endpoint**: `POST /api/users/signup`
- **Description**: Registers a new user.
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password",
    "name": "John Doe",
    "username": "johndoe",
    "user_about": "Hello, I am aspiring to become a successful investor!"
  }
  ```
- **Success Response**: `201 Created`

#### User Login

- **Endpoint**: `POST /api/users/login`
- **Description**: Authenticates a user and returns a token.
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password"
  }
  ```
- **Success Response**: `200 OK`


## USER PROFILE MANAGEMENT


#### Get User Profile

- **Endpoint**: `GET /api/users/profile`
- **Description**: Retrieves the profile of the currently logged-in user.
- **Require Authentication**: Yes
- **Response Body**:
  ```json
  {
    "email": "janedoe@example.com",
    "username": "janedoe",
    "user_intro": "Updated intro message.",
    "profile_pic": "http://example.com/profile_pic.png"
  }
  ```
- **Success Response**: `200 OK`

## Update Profile

- **Endpoint**: `PUT /api/users/profile`
- **Description**: Allows users to update their profile information.
- **Require Authentication**: Yes
- **Response Body**:
  ```json
  {
    "name": "Jane Doe",
    "username": "janedoe",
    "user_intro": "Updated intro message."
  }
  ```
  - **Success Response**: `200 OK`

## Delete Profile

- **Endpoint**: `DELETE /api/users/profile`
- **Description**: Allows users to delete their account.
- **Require Authentication**: Yes
- **Success Response**: `204 No Content`

## STOCKS

### View all Stocks

- **Endpoint**: `GET /api/stocks`
- **Description**: User will be able to view stocks on the site.
- **Require Authentication**: No
- **Success Response**: `200 OK`

## ARTICLES


### View all Articles

- **Endpoint**: `GET /api/articles`
- **Description**: User will be able to view articles on the site.
- **Require Authentication**: No
- **Success Response**: `200 OK`


## WATCHLIST MANAGEMENT


#### Add Stocks to Watchlist

- **Endpoint**: `POST /api/watchlist/{watchlist_id}`
- **Description**: Allows users to add stock to their watchlist.
- **Require Authentication**: Yes
- **Body**:
  ```json
  {
    "stock_id": "STOCK1234",
  }
  ```
- **Success Response**: `201 Created`

#### View Watchlist

- **Endpoint**: `GET /api/watchlist
- **Description**: Allows users to view their watchlisted stocks.
- **Require Authentication**: Yes
- **Success Response**: `200 OK`

#### Update/Edit Watchlist

- **Endpoint**: `PUT /api/watchlist/{watchlist_id}`
- **Description**: Allows users to place watchlisted stocks into different categories on their watchlisted page.
- **Require Authentication**: Yes
- **Body**:
  ```json
  {
    "stock_category": "Currency"
  }
  ```
- **Success Response**: `200 OK`

#### Remove From Watchlist

- **Endpoint**: `DELETE /api/watchlist/{watchlist_id}`
- **Description**: Allows admins to remove stocks from their watchlist.
- **Require Authentication**: Yes
- **Success Response**: `204 No Content`

## ARTICLE MANAGEMENT


#### Pin Articles to Profile

- **Endpoint**: `POST /api/pinned/{pin_id}`
- **Description**: Allows users to pin articles to a section in their profile page.
- **Require Authentication**: Yes
- **Body**:
  ```json
  {
    "article_id": "ARTICLE1234"
  }
  ```
- **Success Response**: `201 Created`

#### View Pinned Articles

- **Endpoint**: `GET /api/pinned`
- **Description**: Allows users to view their pinned articles.
- **Require Authentication**: Yes
-**Success Response**: `200 OK`

#### Update/Edit Pinned Articles

- **Endpoint**: `PUT /api/pinned/{pin_id}`
- **Description**: Allows users to place pinned articles into different categories on their articles page.
- **Require Authentication**: Yes
- **Body**:
  ```json
  {
    "article_category": "Currency"
  }
  ```
- **Success Response**: `200 OK`

#### Remove From Pinned Articles

- **Endpoint**: `DELETE /api/pinned/{pin_id}`
- **Description**: Allows admins to remove articles from their pinned articles page.
- **Require Authentication**: Yes
- **Success Response**: `204 No Content`

## PLANNER MANAGEMENT

#### Add Plan
- **Endpoint**: `POST /api/planner`
- **Description**: Allows users to post in their daily/weekly/monthly categories in their planner section on their user profile page.
- **Require Authentication**: Yes
- **Body**:
  ```json
  {
    "planner_category": "Daily",
    "plan_text": "Read and research trends in oil stocks, and make one promising trade."
  }
  ```
- **Success Response**: `201 Created`

#### View Planner

- **Endpoint**: `GET /api/planner`
- **Description**: Allows users to view submissions in their planner page.
- **Require Authentication**: Yes
- **Success Response**: `200 OK`

#### Update a Plan

- **Endpoint**: `PUT /api/planner/{plan_id}`
- **Description**: Allows users to edit/update existing plan submissions
- **Require Authentication**: Yes
- **Body**:
  ```json
  {
    "planner_category": "Monthly",
    "plan_text": "Review and access trades and progress throughout the past month."
  }
- **Success Response**: `200 OK`

### DELETE PLAN

- **Endpoint**: `DELETE /api/planner/{plan_id}`
- **Description**: Allow users to delete existing plans.
- **Require Authentication**: Yes
- **Success Response**: `204 No content`


## NOTE MANAGEMENT


#### Add a Note

- **Endpoint**: `POST /api/notes`
- **Description**: Allows users to add notes on stocks.
- **Require Authentication**: Yes
- **Body**:
  ```json
  {
  "stock_id": "STOCK1234",
  "note_text": "Noticing an upward trend."
  }
  ```
- **Success Response**: `201 Created`

#### View Notes

- **Endpoint**: `GET /api/notes/{stock_id}`
- **Description**: Allows users to view their notes on a stock.
- **Require Authentication**: Yes
- **Success Response**: `200 OK`

#### Edit a Note

- **Endpoint**: `PUT /api/notes/{note_id}`
- **Description**: Allows users to edit their posted notes on stocks.
- **Require Authentication**: Yes
- **Body**:
  ```json
  {
    "note_text": "Updating trend information"
  }
- **Success Response**: `200 OK`

### Delete Note

- **Endpoint**: `DELETE /api/notes/(note_id)`
- **Description**: Allows users to delete their notes on stocks.
- **Require Authentication**: Yes
- **Success Response**: `204 No Content`

## COMMENT MANAGEMENT


#### Add a Comment

- **Endpoint**: `POST /api/comments`
- **Description**: Allows users to add comments on articles.
- **Require Authentication**: Yes
- **Body**:
  ```json
  {
  "article_id": "ARTICLE1234",
  "comment_text": "This could cause STOCK123 to trend upward in the following weeks."
  }
  ```
- **Success Response**: `201 Created`

#### View Comments

- **Endpoint**: `GET /api/comments/{article_id}`
- **Description**: Allows users to view their comments on an article.
- **Require Authentication**: Yes
- **Success Response**: `200 OK`

#### Edit a Comment

- **Endpoint**: `PUT /api/comments/{comment_id}`
- **Description**: Allows users to edit their posted comments on articles.
- **Require Authentication**: Yes
- **Body**:
  ```json
  {
    "comment_text": "This could cause STOCK123 to trend downward in the following days."
  }
- **Success Response**: `200 OK`

### Delete a Comment

- **Endpoint**: `DELETE /api/comments/(comment_id)`
- **Description**: Allows users to delete their comments on articles.
- **Require Authentication**: Yes
- **Success Response**: `204 No Content`

## BONUS FEATURES ##

## INVESTMENT SIMULATOR


#### Create a Simulated Trade

- **Endpoint**: `POST /api/simulator/trades`
- **Description**: Allow users to create simulated trades with fake currency.
- **Require Authentication**: Yes
- **Body**:
  ```json
  {
   "stock_id": "STOCK1234",
   "trade_amount": 10000,
   "trade_type": "buy",
   "stop_price": 55,
   "limit_order": 53
  }
  ```
- **Success Response**: `201 Created`

#### View Active Trades

- **Endpoint**: `GET /api/simulator/trades`
- **Description**: Allows users to view the status of currently active trades.
- **Require Authentication**: Yes
- **Success Response**: `200 OK`

#### Update A Trade

- **Endpoint**: `PUT /api/simulator/trades/{trade_id}`
- **Description**: Allows users to edit their stop price and limit order on an active trade.
- **Require Authentication**: Yes
- **Body**:
  ```json
  {
    "stop_price": 57,
    "limit_order": 51
  }
- **Success Response**: `200 OK`

### Cancel/Delete Trade

- **Endpoint**: `DELETE /api/simulator/trades/{trade_id}`
- **Description**: Allows users to cash out of an active trade at anytime.
- **Require Authentication**: Yes
- **Success Response**: `204 No Content`


## TRADE HISTORY


### View Trade History

- **Endpoint**: `GET /api/simulator/trades/history
- **Description**: Allow users to view their trade history.
- **Require Authentication**: Yes
- **Success Response**: `200 OK`

### Delete Trade History

- **Endpoint**: `DELETE /api/simulator/trades/history/{item_id}`
- **Description**: Allow users to delete an item from their trade history.
- **Require Authentication**: Yes
- **Success Response**: `204 No Content`
