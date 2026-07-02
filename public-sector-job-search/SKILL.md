---
name: public-sector-job-search
description: Search, verify, and rank China public-sector job opportunities that match a user's resume or career profile. Use when the user wants to find suitable openings from state-owned enterprises, central SOEs, public institutions, civil service exams, selected graduate programs, talent-introduction programs, or official recruitment notices; compare eligibility against resume details; monitor current recruitment information; or produce an application shortlist with official links.
---

# Public Sector Job Search

## Overview

Use this skill to turn a resume or career profile into a verified shortlist of China public-sector opportunities: state-owned enterprises, central SOEs, public institutions, civil service, selected graduates, and local talent-introduction programs.

Always prefer current official sources. Browse the web for live recruitment information unless the user explicitly provides complete source material.

## Workflow

1. Build the candidate profile.
   - Extract education, major, graduation year, work years, industry, skills, certificates, political status, household registration, age, target cities, salary constraints, and exam preferences.
   - If the resume is missing, ask the user to provide it or summarize the profile. If enough context exists, proceed and list assumptions.

2. Define the search scope.
   - Confirm or infer geography, job families, organization types, urgency, and whether the user accepts campus recruitment, social recruitment, contract roles, or only formal headcount roles.
   - Use Chinese search terms by default. Include English only when the candidate profile or target employer suggests it.

3. Search official and high-reliability sources.
   - Read `references/search-sources.md` before composing searches or ranking results.
   - Prioritize official employer pages, government HR/exam portals, SASAC pages, provincial/municipal HR bureaus, personnel examination networks, and public institution recruitment notices.
   - Use third-party job boards only as discovery signals; verify every shortlisted opening with an official notice.

4. Screen eligibility.
   - Check hard constraints first: nationality, age, education, major/catalog, graduation year, political status, work years, hukou, professional certificates, party membership, grassroots experience, and application deadline.
   - Separate "eligible", "likely eligible", "uncertain", and "not eligible". Do not bury disqualifying details.

5. Rank opportunities.
   - Score fit by role relevance, hard-constraint match, region preference, organization stability, application window, and preparation burden.
   - Favor active openings with clear official notices and application channels.

6. Produce an actionable output.
   - Include official links, deadline dates, source dates, match rationale, risk points, and next actions.
   - If no high-fit results are found, report search coverage and suggest adjacent searches rather than inventing openings.

## Output Format

For normal searches, return a compact table with:

- priority
- organization and unit nature
- job title
- location
- application deadline
- key requirements
- match level
- risks or unknowns
- official link

Then add a short action plan:

- applications to submit first
- materials to prepare
- information to confirm manually
- search alerts or follow-up searches to run

## Verification Rules

- Treat recruitment data as time-sensitive. Always include exact dates for deadlines and notice publication dates when available.
- Prefer official notice pages over reposts, screenshots, social media, or forum summaries.
- Do not claim a job is formal headcount, 编制, 央企正式员工, or civil-service establishment unless the source explicitly supports it.
- When a source is ambiguous, say what is ambiguous and how to verify it.
- Keep personal data private. Do not upload resumes or sensitive identity details to external sites.

