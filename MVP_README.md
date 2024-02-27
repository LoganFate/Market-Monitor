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
