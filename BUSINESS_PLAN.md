# RIZQ - BUSINESS PLAN & STRATEGY

**Last Updated:** December 11, 2025
**Status:** Pre-launch / MVP Phase
**Goal:** 10 paying users in 14 days

---

## 🎯 CORE TENETS (Your Rules)

1. **Iterate quickly** - Decide within 1 week if project has traction
2. **Talk to customers daily** - Constant feedback loop
3. **Ship fast, polish later** - Speed over perfection in early stages

---

## 📍 CURRENT POSITION (Week 1 Complete)

**What We Built:**
- Audio upload → Whisper transcription → GPT digest
- Structured cards UI (Summary, Highlights, Insights, Actions, Questions)
- Semantic search with ChromaDB vector storage
- Copy-to-clipboard, animations, clean UX

**What Works:**
- ✅ Core pipeline functional
- ✅ Beautiful UI
- ✅ Local-first development
- ✅ Git version control established

**Technical Debt:**
- Hardcoded backend URL
- No user accounts/auth
- Local-only (not cloud)
- No mobile support yet

---

## 🎯 PIVOT: FROM "MEMORY ENGINE" TO "STUDY TOOL"

### THE PROBLEM

**Original Vision:** "AI Memory Engine for Your Life"
- Too broad
- No clear GTM
- Competes with giants (Apple, Google, Rewind)
- Value delayed (needs 30+ days of data)

**The Pivot:** "Voice Note Intelligence for Students"

### WHY STUDENTS?

1. **Clear pain:** Recording lectures/study sessions but never reviewing them
2. **Instant value:** Summaries + flashcards help them TODAY
3. **Willingness to pay:** $10-15/month if it improves grades
4. **Easy to reach:** Reddit, TikTok, campus marketing
5. **Your product already solves this!**

---

## 🚀 GO-TO-MARKET STRATEGY

### Phase 1: Student Study Tool (Next 14 Days)

**Target Audience:**
- College students (STEM majors, pre-med, law school)
- Ages 18-24
- Struggling with note-taking and exam prep
- Already recording lectures/voice notes

**Value Proposition:**
"Turn messy voice notes into study guides, flashcards, and summaries. Stop forgetting what you learned."

**Key Features (Week 2-4):**
- ✅ Already built: Upload audio → digest
- 🔨 Add: Flashcard generation
- 🔨 Add: Export to Anki/Quizlet
- 🔨 Add: Study mode UI
- 🔨 Add: Microphone recording (no file upload needed)

**Pricing:**
- Free: 5 uploads/month
- Premium: $10/month (unlimited uploads, flashcards, export)

**Marketing Channels:**
1. Reddit (r/college, r/studytips, r/premed, r/lawschool)
2. TikTok demo videos
3. Campus outreach (flyers, student groups)
4. Word of mouth (referral program: give 1 month free for referrals)

### Phase 2: Expand to Founders/Professionals (Month 2-3)

Once we have 50+ paying students:
- Pivot to "meeting memory" for founders
- "Research memory" for academics
- "Client memory" for consultants

Same tech, different positioning.

---

## 📊 BUSINESS MODEL

### Revenue Streams

**Primary:** SaaS Subscription
- Free tier: 5 uploads/month, basic summaries
- Premium: $10/month
  - Unlimited uploads
  - Flashcards + quizzes
  - Export to Anki/Quizlet
  - Priority support

**Future (Phase 3):**
- Team plans ($30/month for 3 users)
- API access for developers
- White-label for universities

### Unit Economics (Current State)

**Costs per user (monthly):**
- Whisper API: ~$3.60 (1 hour of audio/week)
- GPT-4o-mini: ~$2.00 (digests)
- ChromaDB/storage: ~$1.00
- **Total COGS: ~$6.60/user**

**Revenue per user:** $10/month

**Gross margin:** 34% (not great, but acceptable for MVP)

**Improvement path:**
- Self-host Whisper (drops to $0.50/user)
- Batch processing (reduces API costs)
- Scale to 1000+ users (better vendor pricing)

**Target unit economics at scale:**
- COGS: $2/user
- Revenue: $10/user
- Gross margin: 80%

---

## 🎯 SUCCESS METRICS

### 14-Day Goal (Critical)
- [ ] 50 customer conversations
- [ ] 20 beta signups
- [ ] 10 active users (uploaded 3+ times)
- [ ] 5 users say "I would pay $10/month"
- [ ] 3 paying customers (early access pricing)

**If we hit this:** Continue building. We have product-market fit signal.

**If we miss this:** Pivot or kill project. (Per Tenet #1: Decide within 1 week)

### 30-Day Goal
- [ ] 50 paying users ($500 MRR)
- [ ] 70%+ weekly retention
- [ ] 5+ testimonials ("Rizq helped me pass my exam")
- [ ] Viral coefficient >0.3 (1 user brings 0.3 new users)

### 90-Day Goal
- [ ] $5,000 MRR (500 users @ $10/month)
- [ ] Profitable unit economics
- [ ] Ready to approach investors (if desired)

---

## 🏆 COMPETITIVE ANALYSIS

### Direct Competitors

**Otter.ai**
- Strengths: Great transcription, team features
- Weakness: No study tools, no flashcards, $16.99/month
- Our advantage: Student-focused, cheaper, better output format

**Notion AI**
- Strengths: All-in-one workspace
- Weakness: Not voice-first, clunky for audio
- Our advantage: Built for voice notes specifically

**Rewind.ai**
- Strengths: Automatic capture, well-funded
- Weakness: $19/month, desktop-only, privacy concerns
- Our advantage: Cheaper, focused, privacy-first

**Quizlet**
- Strengths: Huge user base, flashcards
- Weakness: Manual input, no voice processing
- Our advantage: Automated flashcard generation from voice

### Why We Can Win

1. **Niche focus:** We're the ONLY tool built for voice notes → study materials
2. **Better UX:** Beautiful cards vs. ugly walls of text
3. **Price:** $10 vs. $15-20 competitors
4. **Speed:** We iterate daily, they iterate quarterly

---

## 🔮 LONG-TERM VISION (5-10 Years)

**Phase 1 (Now):** Study tool for students
**Phase 2 (Year 1):** Memory tool for professionals
**Phase 3 (Year 2):** Proactive AI agent with pattern detection
**Phase 4 (Year 3):** Multi-modal memory (voice + images + location + screen)
**Phase 5 (Year 5):** "Life OS" - the original vision

**Exit scenarios:**
- Acquisition by Notion, Evernote, or education company ($50-200M)
- Continue as independent company (aim for $10M+ ARR)
- Build into platform, pivot to API/infrastructure play

---

## 🚧 KNOWN RISKS

### Risk 1: Student market is broke
**Mitigation:** Offer free tier, target parents paying for college

### Risk 2: AI costs stay high
**Mitigation:** Self-host models, batch processing, price increases

### Risk 3: OpenAI/Google builds this
**Mitigation:** Move fast, own the niche, build moat with personalization

### Risk 4: Privacy concerns
**Mitigation:** Local-first option, E2E encryption, clear data policies

### Risk 5: Can't reach customers
**Mitigation:** Go where students already are (TikTok, Reddit, campus)

---

## 📋 NEXT 7 DAYS - ACTION PLAN

### Day 1-2 (Dec 12-13): Customer Discovery
- [ ] Post on 5 Reddit communities asking "Do you record lectures? What's frustrating?"
- [ ] DM 50 students on Instagram/TikTok
- [ ] Find 3 local college students, buy them coffee, interview them
- [ ] Goal: 20 conversations, 10 people who say "I need this"

### Day 3-4 (Dec 14-15): Build Flashcard Feature
- [ ] Add `/flashcards` endpoint that generates Q&A pairs from transcript
- [ ] Add flashcard UI component
- [ ] Add export to Anki format (.apkg)
- [ ] Test with real study content

### Day 5 (Dec 16): Launch
- [ ] Reddit post: "I built a tool that turns voice notes into study guides (free beta)"
- [ ] TikTok video demo
- [ ] Email the 20 people from Day 1-2
- [ ] Goal: 20 signups

### Day 6-7 (Dec 17-18): Iterate
- [ ] Watch 5 users try the product (screen share)
- [ ] Fix top 3 complaints
- [ ] Ask: "Would you pay $10/month?"
- [ ] Get 3 paying customers (offer early bird: $5/month lifetime)

---

## 💡 KEY INSIGHTS FROM INITIAL FEEDBACK

**What's working:**
- The core idea is sound (memory is valuable)
- You can actually build this (technical moat)
- Students are an accessible market

**What's risky:**
- Original vision is too broad
- Unit economics are tight
- Giants are building similar things

**The path forward:**
- Narrow focus (students only)
- Prove willingness to pay (10 customers in 14 days)
- Build moat through personalization and speed

---

## 🎓 LESSONS TO REMEMBER

1. **"Memory engine" is a feature, not a product.** Lead with the outcome (better grades, less stress).
2. **Talk to customers BEFORE building features.** (You're doing this right!)
3. **Traction > Vision.** Investors fund traction, not slide decks.
4. **Narrow wins.** Own "voice notes for students" before expanding.
5. **Speed is your advantage.** Big companies can't move this fast.

---

## 🔥 THE ULTIMATE QUESTION

**"Can you get 10 college students to pay you $10/month within 14 days?"**

If YES → You have a business. Keep building.
If NO → Pivot or kill. (Per your Tenet #1)

---

**Last updated:** December 11, 2025
**Next review:** December 18, 2025 (after 7-day sprint)
