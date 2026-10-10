# Hate Report · iPhone PWA

An installable, mobile-first Hate Report for the 2026 Hater League, with the approved Week 5 report preserved at `archive/HateReportWeek5.html`.

## What works
- Live, read-only Sleeper API data: standings, current matchup scores, rosters, and transactions. A manual Refresh button fetches current values. Refresh also runs when the app opens.
- Week is read from Sleeper's NFL state, not hardcoded.
- Standings are ordered by wins then points scored. The 'power rankings' are explicitly this same performance-based order, not predictive rankings.
- Week 5 archived HTML is preserved, including its original commentary and design.
- All report sections start collapsed; responsive phone layout and standalone Home Screen display.
- A GitHub Actions publisher runs Tuesdays at 15:00 UTC and writes verified *previous completed week* editorial highlights to `data/editorial.json`. No AI or speculative claims. It will not generate future matchup predictions.

## Deploy and install
1. Create a GitHub repository and upload the **contents** of this folder to the repository root, including `.github/workflows/publish.yml`.
2. In repository Settings → Pages, choose **Deploy from a branch**, branch `main`, folder `/ (root)`. Wait for GitHub to provide the HTTPS site URL.
3. In Settings → Actions → General → Workflow permissions, enable **Read and write permissions** (or otherwise grant the workflow `contents: write`). Enable scheduled workflows for the repository. For private repos, confirm Pages availability for your plan.
4. Visit the GitHub Pages URL on iPhone using **Safari**, tap **Share**, then **Add to Home Screen** and **Add**.
5. The app will update scores whenever opened or Refresh is tapped. The weekly job commits a completed-week recap on Tuesday. Use the Actions tab to run `Publish Hate Report weekly` manually for testing.

## Important limits
- This chat cannot deploy the repository or activate GitHub Actions on your behalf without GitHub authorization. The app must be hosted on HTTPS to be installable and receive updates.
- Live Sleeper calls require internet access. The Week 5 archive and app shell can work offline after a successful visit; current live stats cannot.
- Sleeper's public API may rate-limit or change. There is no retry service or server-side proxy in this starter version.
- Player names: Sleeper matchup rosters use player IDs. `data/players.json` is an optional player-name mapping. A production publisher should generate this file from Sleeper's large player catalog periodically; the app currently falls back to IDs where names are unavailable. This avoids shipping a huge catalog and inventing identities.
- The closest-matchup headline displays the **current score gap**, not a projected spread. At the start of a week it may be 0.0, and this is not a meaningful prediction.
- This is a read-only PWA. It does not alter Sleeper rosters or lineups, and it is not a native App Store IPA.
- If GitHub Actions fails to commit, inspect workflow permissions and branch protection settings.

## Customize
- League ID and your roster ID are defined at the top of `app.js`.
- Brand colors and mobile layouts are in `styles.css`.
- Weekly editorial rules are in `publish_weekly.py`.
- To add AI-generated editorial, connect a secure server-side generation step to the publisher; never put API keys in browser JavaScript.
