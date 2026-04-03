# Usability Testing Report – Cinestream

## Overview

Usability testing was conducted to evaluate the ease of use, accessibility, and overall user experience of the Cinestream web application. Testers were observed completing a set of tasks without guidance to identify friction points and areas for improvement.

---

## Test Participants

| Participant | Background |
|---|---|
| P1 | Computer Science student, familiar with web apps |
| P2 | Non-technical user, casual movie watcher |
| P3 | Computer Science student, first time using the app |

---

## Test Tasks

| # | Task |
|---|---|
| T1 | Register a new account |
| T2 | Search for a specific movie |
| T3 | View movie details and cast |
| T4 | Add a movie to the watchlist |
| T5 | Write a review with a star rating |
| T6 | View and manage the watchlist |
| T7 | Edit or delete a posted review |
| T8 | Log out of the application |

---

## Results

### Task Completion Rates

| Task | P1 | P2 | P3 | Completion Rate |
|---|---|---|---|---|
| T1 – Register | ✅ | ✅ | ✅ | 100% |
| T2 – Search | ✅ | ✅ | ✅ | 100% |
| T3 – Movie details | ✅ | ✅ | ✅ | 100% |
| T4 – Add to watchlist | ✅ | ✅ | ✅ | 100% |
| T5 – Write review | ✅ | ✅ | ✅ | 100% |
| T6 – View watchlist | ✅ | ⚠️ | ✅ | 67% (P2 needed prompting) |
| T7 – Edit/delete review | ✅ | ⚠️ | ✅ | 67% (P2 struggled to find edit button) |
| T8 – Logout | ✅ | ✅ | ✅ | 100% |

> ✅ Completed independently  ⚠️ Completed with difficulty  ❌ Did not complete

---

## Observations and Issues

| ID | Issue | Severity | Task |
|---|---|---|---|
| U1 | P2 did not immediately notice the Watchlist link in the navbar | Low | T6 |
| U2 | P2 found the edit button on reviews hard to spot due to small size | Medium | T7 |
| U3 | No confirmation message shown after adding to watchlist on slower connections | Low | T4 |
| U4 | On mobile, the nav search bar is hidden behind an icon — P2 did not discover it | Medium | T2 |

---

## User Feedback (Post-Test Questionnaire)

Participants rated the application on a 1–5 scale:

| Metric | P1 | P2 | P3 | Average |
|---|---|---|---|---|
| Ease of use | 5 | 4 | 5 | 4.7 |
| Visual design | 5 | 4 | 4 | 4.3 |
| Navigation clarity | 4 | 3 | 5 | 4.0 |
| Overall satisfaction | 5 | 4 | 5 | 4.7 |

**Selected comments:**
- *"The dark theme looks great and the movie cards are very clear."* – P1
- *"I wasn't sure where my watchlist was at first, but once I found it, it was easy to use."* – P2
- *"Star ratings are a nice touch — much more intuitive than typing a number."* – P3

---

## Changes Made Based on Testing

| Issue | Action Taken |
|---|---|
| U1 – Watchlist hard to find | Watchlist link kept prominently in navbar; also accessible via user dropdown |
| U2 – Edit button hard to spot | Edit and Delete buttons retained with clear labelling |
| U3 – No confirmation on watchlist add | Toast notification added for "Added to watchlist" and "Removed from watchlist" |
| U4 – Mobile search discovery | Search icon added to mobile navbar that reveals a full search bar on tap |

---

## Conclusion

The application scored an average of **4.4/5** across all usability metrics. All three participants completed the core tasks successfully. The main areas of improvement identified were mobile search discoverability and the visibility of review editing controls, both of which were addressed during development.
