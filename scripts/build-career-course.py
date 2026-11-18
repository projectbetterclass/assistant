# Builds "From graduate to hired" (CAREER_CURRICULUM) in time-tracker.html: 15 sittings on the Career goal, written in my
# words from the career videos in the youtube-digest library (Leila Hormozi on CVs, interviews, pay and promotion; Dr. K of
# HealthyGamerGG on choosing, confidence and interviews; Vinh Giang on stories and networking; Justin Sung on choosing a
# career; Alex Hormozi on hiring for rate of learning), plus the Dutch rules on holiday pay, probation and pay transparency
# as checked in November 2026. Each sitting runs on your own case: mostly the role you're aiming at after graduating, with
# the revisit on your second choice.
#   python3 scripts/build-career-course.py       -> rewrites the block in time-tracker.html
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from course_block import yt, course, check_videos, check_extras, term_order, lesson_texts, write

K, LH, AH, VG, JS = "HealthyGamerGG", "Leila Hormozi", "Alex Hormozi", "Vinh Giang", "Justin Sung"
DIFF = yt("pqMCdKH9oBQ", K, "How to Find a Job (That You Care About!) | Career Advice", "list every option before you settle, like a differential diagnosis")
PASSION = yt("E4Pp4VMRZKI", JS, "Don't Choose Careers Based on PASSION", "purpose, passion and personality, and what your behaviour says you value")
GRAD = yt("LUD-9Jx3odc", K, "Why You're Not Getting a Job After you Graduate", "why low confidence makes you skip the best jobs, and how to ask for feedback")
NOEXP = yt("UNfXKlfsXto", K, "I Can’t Find a Job Without Experience", "applying for the job you ‘don’t match’, and selling breadth as quick learning")
RESUME = yt("KhJH7wCaFlQ", LH, "5 Steps to learn to Build a Six Figure Resume ($100,000+)", "the CV as an advert: brand line, summary, strengths, results, credentials")
ONLINE = yt("xQPQ0S7RqxA", LH, "F*ck Your Resume Because …", "why your profile online is read before your CV")
INTEL = yt("LhM8zmN0_Mo", AH, "I Hire for Intelligence Over Experience", "intelligence as rate of learning")
PROMO4 = yt("QajLAtEMx7s", LH, "How to Get a Job Promotion [4 CLEVER TIPS]", "do 20% of your boss’s job, better, and learn how the company makes money")
BEFORE = yt("DzbFBgGUGdU", LH, "Watch this BEFORE Your Job Interview", "five last-minute tips, including speaking the ad’s language")
NET = yt("EC1ut0gmspk", VG, "How to Network Like the Top 1% (6 Key Lessons)", "curiosity, research before you meet, FORD, and give first")
TOP10 = yt("grorhKeNklw", LH, "Top 10 Answers to Interview Questions", "what each common question really asks, and the salary question")
ORIGIN = yt("0siE31sqz0Q", VG, "Doing This (Almost) GUARANTEES You Get Hired In A Job Interview!", "an origin story for ‘tell me about yourself’, and the ten usual questions")
WRONG = yt("m9-fUdrHfbs", VG, "You're doing job interviews WRONG!!", "a story instead of adjectives")
INTV = yt("0W92jf5K8Pw", K, "What you Don’t Understand about Job Interviews", "you are there to offer, not to be judged")
FRAME = yt("9tiInaJ_klA", LH, "The BEST interview FRAMEWORK for finding TOP TALENT...that you won't need to fire later..", "the three interviews, from the hirer’s side")
PAYTOO = yt("IN7gbkPtArs", LH, "Millionaire CEO: Are you paying your employees too much?", "fair market value, and why a raise for a busy month goes wrong")
CHEAT = yt("kuTXkRHWcLM", LH, "How To Get Promoted So Fast It Feels Like Cheating", "advocate for your work, plan for tomorrow, manage your time first")

TOP, SECOND = "your top role", "your second-choice role"
L = [
 dict(id="C01", rung="Aim", stage_name="More options than you think", concept="List every option before you pick one",
  teach="Dr. K’s point is that most of us choose a career by ‘monkey see, monkey do’: we reach for whatever is in front of us, what classmates, parents or the first job ad do, and never look at the rest. Doctors are trained against this with a differential diagnosis: list every possibility before settling on one. Do the same with your degree. International Business leads into sales and account management, purchasing and supply chain, marketing, business development, export, consulting, HR, operations, and traineeships that rotate you through several. And when your mind says ‘I can’t do that because…’, don’t close the option: the ‘because’ is usually the next step.",
  task="List at least eight roles you could go for after graduating, from classmates, alumni of your programme on LinkedIn and your internship company, not just the first three that come to mind. Cross none out yet; next to each, write what you’d need that you don’t have. Then pick a top role and a second. Judge: which option did you nearly leave off, and why?",
  co="your degree", rev="your internship company", watch=[DIFF]),
 dict(id="C02", rung="Aim", stage_name="Purpose before passion", concept="Choose on purpose, filter on passion, test personality",
  teach="Justin Sung argues that passion is the weakest reason to pick a career. Interests change a lot over a lifetime, and what feels like passion is often a proxy: liking biology at school and choosing medicine, which is nothing like the job. Choosing on purpose, what you want your work to do in the world, holds up better; then filter by passion, and check personality: a creative person in a job with no room for it wilts even when the purpose fits. Your values show in what you already do, not in what sounds noble, so look at your behaviour. And personality only reveals itself in real experiences, such as your internship.",
  task="For your top role and your second, score purpose, passion and personality from 1–10, each backed by something you actually did: in your internship, a project or a job. Then write one value your behaviour shows, even if it isn’t a flattering one. Judge: which score is a guess rather than evidence, and how could you test it before you graduate?",
  co=TOP, rev=SECOND, watch=[PASSION]),
 dict(id="C03", rung="Aim", stage_name="Read ten ads", concept="Let the ads, not your fears, say what you need",
  teach="Dr. K’s warning to graduates: you are not qualified to judge your own employability. You haven’t hired anyone, so fear fills the gap, and low confidence makes you skip the best jobs and settle for worse ones. Get data instead. Ten real ads for one role tell you what employers ask for: the tools, the languages and the skills that keep coming back, and which are must-haves and which are wishes. ‘Entry level, two years’ experience’ is common, and Dr. K’s advice is to apply anyway: some employers hire for willingness to learn. Note the pay too where an ad gives it, or the CAO scale it mentions.",
  task="Find ten ads for your top role in the Netherlands. Tally every skill, tool and language, mark each must-have or nice-to-have, and write down any pay or CAO scale. Judge: which three things does nearly every ad ask for, and which of them can you already prove?",
  co=TOP, rev=SECOND, watch=[GRAD, NOEXP]),
 dict(id="C04", rung="Prove", stage_name="Close one gap", concept="The skill the ads ask for most, practised every week",
  teach="Leila Hormozi’s method for your strengths: one column with your skills, one with the role’s, and keep the overlap, written specifically, such as ‘assessing customer needs’ or ‘Excel models for purchasing’, not ‘good communicator’. What is left in the ads’ column is your gap. Pick the one that shows up most and practise it every week, with something you can show: a model, a deck, a certificate, a piece of work. Alex Hormozi hires for intelligence, which he defines as rate of learning, so showing that you learn fast counts. Dr. K adds a trap: as your skill rises your confidence can drop, because you start seeing what you don’t know. That is progress, not proof you are behind.",
  task="Make the two columns from your ten ads: your skills and theirs. Keep the ten that overlap, in the ads’ words. Then pick the one gap that appears most and plan it: what you’ll practise each week, for how long, and what you’ll have to show by graduation. Judge: how will an employer see the proof, and not just hear about it?",
  co=TOP, rev=SECOND, after=["C03"], watch=[RESUME, INTEL]),
 dict(id="C05", rung="Prove", stage_name="Proof with a number", concept="Results, not tasks, from your internship",
  teach="Employers don’t want to know what you were in charge of; they want what changed because you were there. Leila Hormozi’s example from a CV: ‘reduced churn from 12% to 8%, adding about $3,000 of lifetime value per account’, followed by how it was done. Write your internship that way: the result, the number, and what you did. If you don’t know the number, that is the task: ask for it before you leave. And ask for one project you can own, ideally one that drives or protects revenue, since every role does one or the other. Taking a piece of your manager’s work off their plate, and doing it better, is how Leila Hormozi says people get noticed.",
  task="Write three results from your internship, each as: what changed, by how much, and what you did. Where a number is missing, write who could give it to you, and ask this week. Then write the short request for a project you could own. Judge: which of your three is a task in disguise, and what would turn it into a result?",
  co="your internship", rev="a study or side project", after=["C02"], watch=[RESUME, PROMO4]),
 dict(id="C06", rung="Prove", stage_name="Feedback, on purpose", concept="Ask people who hire, not your fears",
  teach="Confidence, says Dr. K, mostly comes from feedback from people more experienced than you, and students often get almost none. Many then avoid asking, because as long as nobody says it, they can still hope. Ask anyway, with a narrow question: ‘What would make me more hireable for a first job as X?’, put to your internship supervisor, a teacher, the career office, or someone in the role. Two traps when the answer comes: your mind explains away the praise (‘they’re just being nice’) and jumps straight to the one criticism. Write down what was actually said before you decide what it means.",
  task="Pick two people who have hired for, or work in, your top role and ask them that one question, by message or in person. Write their answers word for word, then sort them into praise, fixes, and things to check. Judge: which part did you want to dismiss, and why?",
  co=TOP, rev=SECOND, after=["C03"], watch=[GRAD]),
 dict(id="C07", rung="Show", stage_name="The CV as an advert", concept="Brand line, summary, strengths, results, credentials",
  teach="Leila Hormozi treats a CV as an advert for one job, not a record of where you have been. Five parts, in order. A brand line under your name: who you are, what you do, and how you work. A two- or three-sentence summary of your experience, with the impact that matters to this employer. Core strengths: the ten overlaps from your two columns, in the ad’s words. Experience as results with numbers, not duties. Then education, certificates and anything else that backs up your skills. Each application gets its own version: the parts stay the same, while the words and the order of the results change with the ad.",
  task="Write your CV for your top role in those five parts, using your ten strengths and three results. Then hold it next to one of your ten ads and underline every word they share. Judge: if the reader stopped after the summary, would they know why to call you?",
  co=TOP, rev=SECOND, after=["C04", "C05"], watch=[RESUME]),
 dict(id="C08", rung="Show", stage_name="LinkedIn first", concept="Your profile is read before your CV",
  teach="Leila Hormozi says she looks at a candidate’s LinkedIn and social media before the CV, so your profile does the CV’s job in public. A headline that names the role you’re aiming at and what you bring. An About that is your summary. Your results under each experience, skills in the words the ads use, and your internship project featured. Speak their language: if the ads say ‘account management’ and ‘B2B’, so do you. A short post about something you learned or built shows how you think, which a CV can’t.",
  task="Rewrite your headline, your About and your internship entry for your top role, using the words from your ten ads. Then draft one short post about a result or lesson from your internship, if your employer is fine with it. Judge: a recruiter spends ten seconds on your profile; what do they now know?",
  co=TOP, rev=SECOND, after=["C04"], watch=[ONLINE, BEFORE]),
 dict(id="C09", rung="Reach", stage_name="Conversations first", concept="Curious first, give first, ask later",
  teach="Vinh Giang’s rules for networking: go in curious about the other person, not looking for what they can do for you, because desperation shows. Research first, such as what they post and where they worked, so you can ask a real question instead of ‘so what do you do?’. Have an opener ready. Ask about them; the FORD prompt is family, occupation, recreation and dreams. Aim for a connection, not a favour, and look for a way to help them. And say what you want out loud: introductions happen when someone knows your goal. For you, that means 20-minute conversations with people who do your top role, many of them alumni of your programme.",
  task="Find five people who do your top role, ideally alumni of your programme. For each, note one thing in their profile you’re curious about, and write a three-sentence message asking for 20 minutes about their path. Then write the three questions you’ll ask. Judge: what could you offer them, and what is the one thing you want them to remember about you?",
  co=TOP, rev=SECOND, after=["C08"], watch=[NET]),
 dict(id="C10", rung="Reach", stage_name="Apply up", concept="Aim at the top half, and at jobs you ‘don’t match’",
  teach="Dr. K describes what low confidence does to a job search: you cross out the best half of the jobs before applying, and pile into the middle, where competition is heaviest. Dr. K applied to about 140 positions and got a research job at Harvard Medical School as its only applicant. A graduate on Dr. K’s stream spent six months failing at ads that asked for two years’ experience, then applied to a job they didn’t match at all and were hired for their willingness to learn; their mixed background became the pitch: a quick learner who sees several sides. So spread your applications: some stretches, mostly matches, a few safe ones, and choose by what you’ll learn there, not only by whether they’ll have you.",
  task="Plan your first ten applications for your top role: three stretches you think are out of reach, five good matches, two safe ones. For each, write the one thing you would learn there. Judge: which stretch did your fear try to cross out, and what is the worst that happens if you apply?",
  co=TOP, rev=SECOND, after=["C07"], watch=[GRAD, NOEXP]),
 dict(id="C11", rung="Interview", stage_name="Tell me about yourself", concept="Your pitch for this role, with one short story",
  teach="Leila Hormozi says ‘tell me about yourself’ really asks what value you bring to this role, and that a hiring manager often decides in the first 15 minutes. Her structure: where you’ve been (title and results), your biggest strength with proof, and why that fits this job. Vinh Giang adds what makes it stick: a short true story instead of adjectives. Don’t say ‘I take initiative’; tell the one moment that shows it, then link it to the role. Adjectives ask the interviewer to believe you; a story gives evidence and builds rapport. Keep it to about two minutes, rehearsed but not memorised word for word.",
  task="Write your answer for your top role: your internship and its best result, your strength with proof, why this job, and the one short story that shows the trait the ads want most. Say it aloud and time it. Judge: which sentence is an adjective you could replace with evidence?",
  co=TOP, rev=SECOND, after=["C09", "C10"], watch=[TOP10, ORIGIN, WRONG]),
 dict(id="C12", rung="Interview", stage_name="The question behind the question", concept="Each usual question asks something else",
  teach="Leila Hormozi translates the usual questions. ‘Why here?’ asks how much research you did: answer from their mission and values, not the pay or the perks. ‘Your weakness?’ wants a real one, not ‘perfectionist’, ideally not central to the role, plus what you’re doing about it. ‘What makes you unique?’ means ‘why you over the other five’: name a rare pairing, such as numbers plus people skills. ‘Career plans?’ asks how long you’ll stay. For a challenge or conflict, the usual structure is STAR: situation, task, action, result. And Dr. K’s mindset: you are not there to be judged, but to offer what you have and let them decide whether it fits.",
  task="For one real employer in your top role, write answers to: why here (from their site and values), your real weakness and what you’re doing about it, your unique pairing, and one STAR story from your internship. Judge: which answer is about you rather than about them, and how would you turn it round?",
  co=TOP, rev=SECOND, after=["C09"], watch=[TOP10, INTV]),
 dict(id="C13", rung="Interview", stage_name="Their side of the table", concept="Three rounds: history, skill, fit",
  teach="Leila Hormozi hires through three interviews, and knowing them tells you what to bring. First, the hiring manager checks your history, qualifications and values against your CV. Second, a skills round, often with future colleagues: real scenarios, your portfolio, or an assignment; whatever you show here is taken as the best you will ever do. Third, a gatekeeper checks culture fit and whether the job is right for you, sometimes by telling you the hard parts. So bring proof, such as your internship project, treat an assignment as the job itself, and ask your own questions: a line from the ad, ‘how would I exceed your expectations?’, what the first 30, 60 and 90 days look like, and how people learn and work together there.",
  task="Prepare for the skills round for your top role: pick the one piece of work you’d show, and write how you’d walk through it in three minutes. Then write your five questions for them, including one about how new people learn there. Judge: if they set an assignment, how would you show it is your best?",
  co=TOP, rev=SECOND, after=["C10"], watch=[FRAME, BEFORE]),
 dict(id="C14", rung="Pay", stage_name="Know your number", concept="A researched range, the whole package, and the Dutch rules",
  teach="Leila Hormozi’s advice on the salary question: research before you’re asked. Look up pay for the role at your level, check what similar companies pay, and give a range with your target in the upper half, citing your research. A number far above the market hurts you; a reasoned range shows you think. In the Netherlands, compare packages, not just gross monthly pay: by law you get at least 8% holiday pay on top, and a CAO may add a 13th month, a pension and fixed scales. Read the probation rule too: none on contracts of six months or less, at most one month up to two years, at most two months on longer or permanent ones. A Dutch pay-transparency law, aimed at 1 January 2027 but not yet passed, will make employers give the starting pay or range before you negotiate, and stop them asking what you earn now.",
  task="Build your range for your top role from at least five sources: ads that give pay, a CAO scale if the sector has one, salary sites, and what alumni told you. Write the gross monthly low, target and high, then the yearly package with 8% holiday pay and any 13th month. Judge: what exactly will you say when they ask for your expectation?",
  co=TOP, rev=SECOND, after=["C12"], watch=[TOP10, PAYTOO],
  read=["Rijksoverheid: holiday pay (vakantiegeld) is at least 8% of your gross yearly salary",
        "Rijksoverheid: probation (proeftijd) — none on contracts of 6 months or less; at most 1 month under 2 years; at most 2 months for 2 years or longer, or permanent",
        "Wet loontransparantie (EU directive 2023/970): aimed at 1 January 2027, not yet passed (November 2026)"]),
 dict(id="C15", rung="Pay", stage_name="Get paid for what you do", concept="Make your work visible, then check the market yearly",
  teach="Raises follow value, and value counts only when someone sees it. Leila Hormozi’s first habit for promotion is to switch from executing to advocating: a weekly note to your manager on what you did and what it changed. Then work on tomorrow as well as today: write where your part of the work should be in a year, and what it needs. Manage your own time before you ask to manage others. Leila Hormozi also warns employers against raises for one busy month, because pay should track fair market value for your skills; so once a year, check the market and bring your evidence. Dr. K mentions research suggesting people who move jobs every two to five years earn the most, though it depends on the field.",
  task="Draft your first weekly note to a manager: three things you did and what each changed. Then set a yearly date to check your pay, with the sources from your range, your results since last time, and the number you’ll ask for. Judge: what would make you change jobs rather than ask for a raise?",
  co="your first job", rev="your internship now", after=["C13"], watch=[CHEAT, PAYTOO]),
]

# ---- the walk-through format: a short idea, a walk-through with a worked example, the thread, a worked answer, a revisit ----
# The worked examples use real Dutch vacancies for junior supply-chain roles, as checked in November 2026, with their links.
RANDSTAD = ("Randstad Professional · Junior consultant supply chain (vacancy, Nov 2026)", "https://www.randstadprofessional.nl/vacatures/9217249/junior-consultant-supply-chain")
LEVVL = ("Levvl · Junior supply chain consultant (vacancy, Nov 2026)", "https://www.levvl.nl/vacatures/junior-supply-chain-consultant")
DELOITTE = ("Deloitte · Junior consultant supply chain & network operations (vacancy, Nov 2026)", "https://werkenbijdeloitte.nl/vacature/junior-consultant-supply-chain-and-network-operations-ref4117e/")
FCAMPINA = ("FrieslandCampina · Global traineeship supply chain (Nov 2026)", "https://careers.frieslandcampina.com/nld/nl/job_requisition_entity/2278495")
SIRE = ("SIRE Life Sciences, Rotterdam · Supply chain analyst (vacancy, Nov 2026)", "https://www.werkzoeken.nl/vacature/13872367-supply-chain-analyst")
DSV = ("DSV, Rotterdam · Junior supply chain consultant (vacancy, Nov 2026)", "https://jobs.dsv.com/job/Rotterdam-Junior-Supply-Chain-Consultant-ZH-3089-JW/1402941733/")
def at(sec, src): return dict(sec, s=src[0], u=src[1])

# the salary range in C14, from the two ads that give pay
PAY_RANDSTAD, PAY_LEVVL_LO, PAY_LEVVL_HI = 3000, 2750, 3500
LOW, TARGET, HIGH = 2800, 3200, 3500
YEAR = TARGET * 12; HOLIDAY = round(YEAR * 0.08); YEAR_H = YEAR + HOLIDAY; YEAR_13 = YEAR_H + TARGET
def eur(x): return "€{:,.0f}".format(x)

EXTRA = {}
EXTRA["C01"] = dict(
  teach="Most of us pick a career by copying what is in front of us: classmates, parents, the first ad we see. Doctors are trained against this with a differential diagnosis: list every possibility before settling on one. Do the same with your degree, and when your mind says ‘I can’t do that because…’, keep the option: the ‘because’ is usually the next step.",
  walk=[{"h": "Why we stop at three", "p": ["Dr. K calls it ‘monkey see, monkey do’: you reach for what classmates, parents or the first job ad do, and never look at the rest. The fix is a habit from medicine: write every option down before you judge any of them."]},
        {"h": "Where a business degree leads", "l": ["Sales and account management.", "Purchasing, planning and supply chain.", "Operations and logistics.", "Consulting, often through a traineeship first.",
                                                    "Marketing and business development.", "Export and international trade.", "HR.", "Traineeships that rotate you through several of these."]},
        {"h": "Keep the ‘because’", "p": ["‘I can’t be a consultant because I don’t have a master’s’ isn’t a reason to cross it out. It’s a fact to check, and often a step: some consultancies hire bachelor’s graduates into traineeships, and the master’s can come later."]},
        {"h": "Where it goes wrong", "l": ["Crossing options out before they’re written down.", "Listing only the roles classmates take.", "Judging by the job title instead of the work it involves."]},
        {"h": "Worked: one interest, eight roles", "p": ["Take an interest in operations and supply chain. Eight roles, with what each needs: junior supply chain consultant (a traineeship, Dutch, some experience); supply chain analyst (Power BI, SQL); demand or supply planner (Excel, an ERP system); buyer (negotiation, a purchasing course); logistics coordinator (on-the-floor experience); a rotating graduate traineeship (applications a year ahead); order or customer operations (Dutch and English); a Big 4 supply chain consultant (a university master’s)."]},
        {"h": "Your turn: your degree", "p": ["At least eight roles from classmates, alumni on LinkedIn and your internship company, each with what you’d need; then a top role and a second."]}],
  key=[{"t": "A good answer looks like", "l": ["Eight or more roles, from at least two of the three sources, none crossed out.", "Next to each, one concrete thing you’d need: a tool, a degree, a language, a kind of experience.",
        "A top role and a second, each with one line on why.", "The option you nearly left off, named, with the ‘because’ that almost stopped you."]}],
  thread={"n": "C02 · choosing between them on purpose, not on passion"},
  rtask="For your internship company: list every role there you could grow into in two years, and what each would need from you.",
  rkey=[{"t": "Short answer", "l": ["At least five roles, from the organisation chart or the company’s vacancies, each with one gap. The useful find is a role you didn’t know existed there."]}])

EXTRA["C02"] = dict(
  teach="Passion is the weakest reason to pick a career: interests change, and what feels like passion is often a stand-in for something else. Choose on purpose, what you want your work to do; filter by passion; then test personality, which only shows in real experience. Your values show in what you already do, not in what sounds noble.",
  walk=[{"h": "Three filters, in this order", "l": [["Purpose.", "What you want your work to do in the world, or for the people around you."], ["Passion.", "A filter, not the starting point: interests change a lot over a life."],
                                                     ["Personality.", "Whether the daily work suits you; only real experience shows it, such as an internship or a part-time job."]]},
        {"h": "Why passion misleads", "p": ["Justin Sung’s example: liking biology at school and choosing medicine, which is nothing like the job. The passion was for the subject, not the work."]},
        {"h": "Look at what you do", "p": ["Your values show in your behaviour. If you keep rebuilding spreadsheets to make them faster, that says more about you than a line about ‘wanting to help people’."]},
        {"h": "Where it goes wrong", "l": ["Scoring from imagination instead of from something you did.", "Writing only flattering values.", "Ignoring personality: a people person in a job with no people wilts, even when the purpose fits."]},
        {"h": "Worked: consultant or analyst", "p": ["Someone weighing a supply chain consultant role against an analyst role might score: purpose 8 and 7 (fixing how a company runs, from suggesting changes at work); passion 6 and 8 (enjoys building dashboards, from evenings spent on them); personality 7 and 5 (likes explaining things to people, from tutoring). The analyst passion score has evidence; the consultant personality score is a guess until they’ve sat in a client meeting."]},
        {"h": "Your turn: your top role", "p": ["Purpose, passion and personality, 1–10, for your top role and your second, each backed by something you did."]}],
  key=[{"t": "A good answer looks like", "l": ["Six scores, each with a real thing you did behind it, not a feeling.", "One value your behaviour shows, even an unflattering one, such as ‘I like being right’.",
        "The score that’s a guess, named, with a test before graduation: shadow someone for a day, ask for a project in that area, or talk to two people in the role."]}],
  thread={"b": "C01 · every option on the table", "n": "C03 · what ten real ads ask for"},
  rtask="Score your second-choice role on purpose, passion and personality, with evidence for each.",
  rkey=[{"t": "Short answer", "l": ["Three scores with evidence. If the second choice wins on the evidence and loses only on guesses, test it before you rule it out."]}])

EXTRA["C03"] = dict(
  teach="You can’t judge your own employability before you’ve hired anyone, so fear fills the gap and you skip the best jobs. Get data instead: ten real ads for one role show what employers ask for again and again, which of it is a must-have, and what it pays. ‘Entry level, two years’ experience’ is common; apply anyway.",
  walk=[{"h": "How to read an ad", "l": [["Must-haves.", "Usually under ‘eisen’ or ‘what you bring’: degree level, language, years."], ["Nice-to-haves.", "‘Een pré’ in Dutch ads: count them, but don’t treat them as walls."],
                                          ["Tools.", "Excel, Power BI, SQL, an ERP system such as SAP."], ["Pay.", "A range, or a CAO scale: the collective agreement that sets pay steps for a sector."]]},
        {"h": "Why ten", "p": ["One ad tells you about one company. Ten tell you about the role: what keeps coming back is what the market wants, and what appears once is one manager’s wish."]},
        {"h": "Where it goes wrong", "l": ["Reading three ads and calling it research.", "Counting the same vacancy twice, once from the company and once from an agency.", "Treating every line as a must-have, and talking yourself out of applying."]},
        at({"h": "Worked: junior supply chain consultant, November 2026", "p": ["Across the ads: a degree in supply chain, logistics or business at HBO or university level; fluent Dutch; some internship or part-time experience in the field; graduated within two years. Pay where given: €3,000 a month on a two-year traineeship, and €2,750–3,500 elsewhere. The Big 4 ask for a university master’s; agencies and smaller consultancies take HBO. Analyst ads add Power BI and SQL."]}, RANDSTAD),
        {"h": "Your turn: ten ads", "p": ["Ten ads for your top role in the Netherlands, tallied: every skill, tool and language, must-have or nice-to-have, and any pay."]}],
  need=[{"k": "Where to look", "v": "LinkedIn, Indeed, werkzoeken.nl, consultancy.nl", "n": "and the careers pages of companies you’d like"},
        {"k": "Dutch ad words", "v": "eisen = must-have · een pré = nice to have", "n": "CAO = the sector’s collective pay agreement"}],
  key=[{"t": "A good answer looks like", "l": ["A tally: each requirement with how many of the ten ads ask for it, marked must-have or nice-to-have.", "Pay from every ad that gives it, and the CAO if one is named.",
        "The top three requirements, and for each: proof you have now, or none yet.", "For a junior supply chain consultant in November 2026, the top three were the degree, fluent Dutch and some experience in the field; tools came next."]}],
  thread={"b": "C02 · a top role and a second", "n": "C04 · closing the gap the ads show; C06 · feedback from people who hire"},
  rtask="Ten ads for your second-choice role: the top three requirements, and which of them your top role’s ads share.",
  rkey=[{"t": "Short answer", "l": ["The overlap is worth most: a skill both roles ask for is the one to build first, because it keeps both doors open."]}])

EXTRA["C04"] = dict(
  teach="Put your skills next to the skills the ads ask for. Keep the overlap, in the ads’ words; what’s left is your gap. Close the one that appears most, every week, with something an employer can see: a model, a dashboard, a project. Showing that you learn fast counts, because many employers hire for rate of learning.",
  walk=[{"h": "Two columns", "p": ["Leila Hormozi’s method: one column with your skills, one with the role’s. The overlap becomes your list of strengths, written specifically, such as ‘Excel models for purchasing’, not ‘good communicator’. What’s left in the role’s column is the gap."]},
        {"h": "One gap, with proof", "l": ["Pick the gap that appears in the most ads.", "Practise it every week, at a set time.", "End with something an employer can open: a file, a dashboard, a write-up."]},
        {"h": "Rate of learning", "p": ["Alex Hormozi hires for intelligence, defined as rate of learning. A project you built in three months shows that better than a certificate that took a weekend."]},
        {"h": "Skill up, confidence down", "p": ["Dr. K’s warning: as your skill rises, your confidence can drop, because you start seeing what you don’t know. That is progress, not proof you’re behind."]},
        {"h": "Where it goes wrong", "l": ["Five gaps at once, none closed.", "Courses with nothing to show at the end.", "A certificate in something the ads don’t ask for."]},
        at({"h": "Worked: Power BI as the gap", "p": ["Analyst ads for supply chain name Power BI and SQL more than anything else. A plan: one module of Microsoft’s free Power BI training a sitting, twice a week, and by graduation one dashboard on supply-chain data with three findings, shown as screenshots on LinkedIn and the file on GitHub."]}, SIRE),
        {"h": "Your turn: your gap", "p": ["The two columns from your ten ads, the gap that appears most, and its weekly plan with what you’ll show by graduation."]}],
  key=[{"t": "A good answer looks like", "l": ["Ten strengths in the ads’ own words.", "One gap, chosen because it appears most, not because it’s the most fun.",
        "A weekly slot (‘Tuesday and Thursday after dinner, 30 minutes’) and a thing to show by a date.", "How an employer will see it: a link on the CV, a featured project on LinkedIn, or a walk-through in an interview."]}],
  thread={"b": "C03 · what the ads ask for", "n": "C07 · the CV that shows it"},
  rtask="The same two columns for your second-choice role: which gap appears most, and is it the same one?",
  rkey=[{"t": "Short answer", "l": ["If the gap is the same, your plan already serves both roles. If not, keep the top role’s plan and note the second gap for later; two at once usually closes neither."]}])

EXTRA["C05"] = dict(
  teach="Employers don’t want what you were in charge of; they want what changed because you were there. Write each experience as a result: what changed, by how much, and what you did. If you don’t know the number, the task is to ask for it before you leave, and to ask for one project you can own.",
  walk=[{"h": "Results, not tasks", "p": ["Leila Hormozi’s example from a CV: ‘reduced churn from 12% to 8%, adding about $3,000 of lifetime value per account’, followed by how it was done. The duty is the background; the change is the headline."]},
        {"h": "The formula", "l": ["What changed.", "By how much, in numbers or a percentage.", "What you did to make it happen."]},
        {"h": "No number yet", "p": ["Ask your supervisor before you leave: ‘What changed in this team’s numbers while I was here, and what did my work add?’ If the figures are confidential, a percentage or a before-and-after is usually fine."]},
        {"h": "Own one project", "p": ["Ask for one piece of work you can own, ideally one that brings in or protects money, since every role does one or the other. Taking part of your manager’s work off their plate, and doing it well, is how people get noticed."]},
        {"h": "Where it goes wrong", "l": ["‘Responsible for…’: a duty dressed as a result.", "A number you couldn’t explain if asked.", "A confidential figure on a public CV."]},
        {"h": "Worked: one line rewritten", "p": ["Before: ‘Handled customer emails for the webshop.’ After: ‘Cut the reply time on customer emails from two days to under one by sorting them into five standard answers, which the team now uses.’ Same job, but now it shows what changed and what you did."]},
        {"h": "Your turn: your internship", "p": ["Three results from your internship in the formula, the person who can give you a missing number, and the request for a project you could own."]}],
  key=[{"t": "A good answer looks like", "l": ["Three lines, each starting with the change: ‘Cut…’, ‘Raised…’, ‘Built…’.", "A number in each, or the name of who will give you one this week.",
        "A two-sentence request for a project: what you’d take on, and what it would change for the team.", "The task in disguise, spotted and rewritten."]}],
  thread={"b": "C02 · what your behaviour says you value", "n": "C07 · results as the heart of the CV"},
  rtask="Three results from a study or side project, in the same formula.",
  rkey=[{"t": "Short answer", "l": ["A study project counts if something changed: a model that answered a question, a tool people used, a grade on a real client case. Write it the same way: the change, the number, what you did."]}])

EXTRA["C06"] = dict(
  teach="Confidence mostly comes from feedback from people more experienced than you, and students get very little. Ask for it with one narrow question, to people who hire or do the role. When the answer comes, write down what was said before deciding what it means: your mind will explain away the praise and jump to the one criticism.",
  walk=[{"h": "Why ask at all", "p": ["Dr. K’s point: as long as nobody tells you, you can keep hoping, so many students avoid asking. But without feedback, fear fills the gap."]},
        {"h": "One narrow question", "p": ["‘What would make me more hireable for a first job as a supply chain analyst?’ is answerable in a minute. ‘What do you think of me?’ isn’t."]},
        {"h": "Who to ask", "l": ["Your internship supervisor.", "A teacher who knows the field.", "The career office.", "Someone who does the role now, or hires for it."]},
        {"h": "Hearing the answer", "l": ["Write it down word for word.", "Watch for ‘they’re just being nice’ about the praise.", "Don’t argue; ask one follow-up question instead."]},
        {"h": "Where it goes wrong", "l": ["Asking friends, who won’t say the hard part.", "A question too vague to answer.", "Acting on one opinion without checking it against the ads."]},
        {"h": "Worked: one answer, sorted", "p": ["A supervisor says: ‘Your analysis is solid, but you rarely speak up in meetings, and you should learn SQL.’ Praise: the analysis. Fix: speaking up, practised in one meeting a week. Check: SQL. Is it in the ads for your role? If it is, it joins your gap list; if not, it’s one person’s view."]},
        {"h": "Your turn: two people", "p": ["Your question to two people who hire for or work in your top role, their answers word for word, sorted into praise, fixes and things to check."]}],
  key=[{"t": "A good answer looks like", "l": ["Two named people and the exact question sent.", "Their answers in their words, not your summary.", "Each point sorted: praise, fix, or check against the ads.", "The part you wanted to dismiss, named."]}],
  thread={"b": "C03 · the ads, as the check on any advice", "n": "C07 · turning it into the CV"},
  rtask="Ask one person in your second-choice role the same question, and compare the answer with the first two.",
  rkey=[{"t": "Short answer", "l": ["What all three say is the strongest signal. What only one says, check against the ads before acting on it."]}])

EXTRA["C07"] = dict(
  teach="A CV is an advert for one job, not a record of where you’ve been. It has five parts, in order: a brand line, a short summary, your core strengths in the ad’s words, experience as results with numbers, then education and credentials. The parts stay the same for every application; the words and the order of the results change with each ad.",
  walk=[{"h": "The five parts", "l": [["Brand line.", "Under your name: who you are, what you do, how you work."], ["Summary.", "Two or three sentences: your experience and the impact this employer cares about."],
                                      ["Core strengths.", "The overlap from your two columns, in the ad’s words."], ["Experience.", "Results with numbers, newest first."], ["Education and credentials.", "Degree, certificates, and anything that proves a strength."]]},
        {"h": "One CV per ad", "p": ["Keep a master CV with everything. For each application, copy it, then change the words to the ad’s and move the results that matter most for this job to the top."]},
        {"h": "Dutch habits", "l": ["One or two pages.", "In the language of the ad.", "A photo is common in the Netherlands but not required."]},
        {"h": "Where it goes wrong", "l": ["A list of duties.", "The same CV for every ad.", "Adjectives as strengths: ‘hard-working, team player’."]},
        {"h": "Worked: a brand line and a summary", "p": ["Brand line: ‘Operations and supply chain graduate who turns order data into decisions.’ Summary: ‘Business graduate specialised in operations and supply chain, with two years of part-time operations work and a Power BI project that traced a drop in on-time delivery to one carrier switch. Looking for a consultancy traineeship where analysis turns into advice.’ Every phrase answers something the ads asked for."]},
        {"h": "Your turn: your top role", "p": ["Your CV for one ad, in the five parts, then underline every word it shares with the ad."]}],
  key=[{"t": "A good answer looks like", "l": ["A brand line a stranger could repeat after one reading.", "A summary that names the role and one result.", "Strengths copied from the ad’s wording, not yours.",
        "Results with numbers, newest first.", "If the reader stopped after the summary, they’d know why to call you."]}],
  thread={"b": "C04 · your strengths and your gap; C05 · results with numbers", "n": "C08 · the same story on LinkedIn"},
  rtask="The same CV, adapted to one ad for your second-choice role: what moved, and what changed words?",
  rkey=[{"t": "Short answer", "l": ["The parts stay; the summary’s role, the strengths’ wording and the order of the results change. If nothing moved, the CV isn’t aimed yet."]}])

EXTRA["C08"] = dict(
  teach="Recruiters often look at your LinkedIn before your CV, so your profile has to do the CV’s job in public. A headline naming the role you’re aiming at and what you bring, an About that is your summary, results under each experience, skills in the ads’ words, and one project featured. A short post shows how you think, which a CV can’t.",
  walk=[{"h": "The parts that get read", "l": [["Headline.", "The role you’re aiming at and what you bring, not ‘student at…’."], ["About.", "Your CV summary, a little warmer."],
                                                ["Experience.", "The same results as your CV."], ["Skills.", "In the words the ads use."], ["Featured.", "One project, with a picture."]]},
        {"h": "Speak their language", "p": ["If the ads say ‘supply chain planning’ and ‘Power BI’, so does your profile. Recruiters search with those words."]},
        {"h": "One post", "p": ["A short post about something you learned or built: three lines and a picture. It shows how you think, and it puts your name in front of people who don’t know you yet."]},
        {"h": "Where it goes wrong", "l": ["A headline that only says ‘student’.", "An empty About.", "Posting your employer’s confidential numbers."]},
        {"h": "Worked: a headline, before and after", "p": ["Before: ‘Student International Business’. After: ‘Operations and supply chain | Power BI dashboards on order and freight data | open to junior consultant and analyst roles’. The second shows up when a recruiter searches for any of those words."]},
        {"h": "Your turn: your profile", "p": ["Your headline, About and internship entry in the ads’ words, and a draft post about one result or lesson."]}],
  key=[{"t": "A good answer looks like", "l": ["A headline with the target role and two skills from the ads.", "An About of three to five sentences, matching your CV summary.",
        "Results, not duties, under each experience.", "One featured project, and a short post drafted, cleared with your employer if it mentions work."]}],
  thread={"b": "C07 · the CV", "n": "C09 · conversations with people in the role"},
  rtask="Rewrite your headline for your second-choice role. Could one headline serve both?",
  rkey=[{"t": "Short answer", "l": ["Often yes, if both roles share the skills: lead with the shared skills and name both roles. If they don’t share any, pick the top role for the headline and leave the second to your CV."]}])

EXTRA["C09"] = dict(
  teach="Networking works when you’re curious about the other person rather than after what they can do for you: desperation shows. Research them first so you can ask a real question, aim for a connection rather than a favour, look for a way to help them, and say what you want out loud, because introductions happen when someone knows your goal.",
  walk=[{"h": "Curious, not desperate", "p": ["Vinh Giang’s first rule: go in wanting to learn about them. People feel when they’re being used as a ladder."]},
        {"h": "Before you meet", "l": [["Research.", "What they post, where they worked, what changed in their career."], ["An opener.", "One specific thing you noticed and are curious about."],
                                       ["FORD.", "If the talk stalls: family, occupation, recreation, dreams."]]},
        {"h": "Give first", "p": ["Look for one way to help: an article on something they mentioned, an introduction, notes from a talk. A small gift makes the next conversation easy."]},
        {"h": "Say what you want", "p": ["At the end, say your goal plainly: ‘I’m aiming for a junior supply chain role after graduating next summer.’ Introductions only happen when someone knows what to introduce you for."]},
        {"h": "Where it goes wrong", "l": ["Asking for a job in the first message.", "A message that could go to anyone.", "No thank-you or follow-up afterwards."]},
        {"h": "Worked: a three-sentence message", "p": ["‘Hi Sanne, I saw you moved from a logistics traineeship into supply chain consulting; I’m graduating in operations and supply chain and curious how that switch worked. Could I ask you three questions in a 20-minute call next week? I’d be glad to send you my notes from the warehouse automation talk in return.’ Specific, short, and it offers something."]},
        {"h": "Your turn: five people", "p": ["Five people in your top role, ideally alumni of your programme, a three-sentence message to each, and your three questions."]}],
  key=[{"t": "A good answer looks like", "l": ["Five names, each with one specific thing you’re curious about.", "Messages of three sentences: what you noticed, the ask (20 minutes), what you offer.",
        "Three questions about their path, not about job openings.", "The one sentence you want them to remember about you."]}],
  thread={"b": "C08 · a profile worth looking at", "n": "C10 · where to apply"},
  rtask="Two people in your second-choice role: a message to each, and one question you’d only ask them.",
  rkey=[{"t": "Short answer", "l": ["The question only they can answer is usually the honest one: what the job is like on a bad day, or what they’d do differently."]}])

EXTRA["C10"] = dict(
  teach="Low confidence makes you cross out the best half of the jobs before applying and pile into the middle, where competition is heaviest. Spread your applications instead: some stretches, mostly matches, a few safe ones. Apply to jobs you don’t fully match; some employers hire for willingness to learn. Choose by what you’ll learn there, not only by whether they’ll have you.",
  walk=[{"h": "What fear does to a search", "p": ["Dr. K applied to about 140 positions and got a research job at Harvard Medical School as its only applicant: the job others had talked themselves out of."]},
        {"h": "Three, five, two", "l": [["Three stretches.", "Jobs that feel out of reach."], ["Five matches.", "You meet most must-haves."], ["Two safe ones.", "You’d very likely get them."]]},
        {"h": "Choose by learning", "p": ["For each job, write the one thing you’d learn there. A first job is mostly training; the best one teaches you most."]},
        {"h": "Where it goes wrong", "l": ["Only safe applications.", "The same CV sent to all ten.", "Crossing out an ad for one missing must-have."]},
        at({"h": "Worked: ten applications for supply chain, November 2026", "l": [["Stretches.", "A Big 4 supply chain role (asks a university master’s); a rotating graduate traineeship at a food company (bachelor’s is enough, but few places); a boutique consultancy."],
                                                                                  ["Matches.", "Junior supply chain consultant traineeships at agencies (HBO, Dutch, some experience, €3,000 a month); a junior supply chain consultant at a logistics firm in Rotterdam; a supply chain analyst in Rotterdam (MBO or HBO, Power BI and SQL); two more like these."],
                                                                                  ["Safe.", "A supply planner and a logistics coordinator role."]]}, DSV),
        {"h": "Your turn: your first ten", "p": ["Three stretches, five matches and two safe ones for your top role, each with what you’d learn there."]}],
  key=[{"t": "A good answer looks like", "l": ["Ten named jobs: three stretches, five matches, two safe ones.", "One thing you’d learn at each.", "The stretch your fear wanted to cross out, kept on the list.",
        "Dates: the graduate traineeships open applications a year ahead, so they go in the calendar now."]}],
  thread={"b": "C07 · a CV aimed at each ad", "n": "C11 · the first interview question"},
  rtask="Three stretches, five matches, two safe ones for your second-choice role.",
  rkey=[{"t": "Short answer", "l": ["If the second role’s matches outnumber the first role’s, that’s worth knowing: it may be the faster way in, and a step towards the first."]}])

EXTRA["C11"] = dict(
  teach="‘Tell me about yourself’ asks what value you bring to this role, and many hiring managers decide in the first fifteen minutes. Answer in three parts: where you’ve been, with a result; your biggest strength, with proof; and why that fits this job. Swap adjectives for one short true story: an adjective asks them to believe you, a story gives evidence.",
  walk=[{"h": "What it really asks", "p": ["Leila Hormozi: not your life story, but why you, for this job. It’s often the first question, and first impressions stick."]},
        {"h": "Three parts", "l": [["Where you’ve been.", "Your degree and your last role, with one result."], ["Your strength.", "The one the ads want most, with proof."], ["Why this job.", "How that strength fits what they need."]]},
        {"h": "A story, not adjectives", "p": ["Vinh Giang’s rule: don’t say ‘I take initiative’; tell the one moment that shows it, then link it to the role. A story builds rapport and gives evidence at once."]},
        {"h": "About two minutes", "p": ["Rehearsed, not memorised word for word. Time it out loud."]},
        {"h": "Where it goes wrong", "l": ["Starting from childhood.", "Reading your CV aloud.", "A list of adjectives."]},
        {"h": "Worked: an adjective swapped for a story", "p": ["Instead of ‘I’m proactive’: ‘In my second month on the customer team, I noticed most emails asked the same five questions. I wrote five standard answers, the team started using them, and reply times dropped from two days to one. That’s the kind of thing I’d like to do for clients as a consultant: spot the pattern, then fix it at the source.’"]},
        {"h": "Your turn: your two minutes", "p": ["Your answer for your top role in the three parts, with one story, said aloud and timed."]}],
  key=[{"t": "A good answer looks like", "l": ["Under two and a half minutes, out loud.", "One result with a number in the first part.", "One story that shows the trait the ads want most.", "A last line that links you to this job, not to any job."]}],
  thread={"b": "C09 · what people in the role told you; C10 · where you’re applying", "n": "C12 · what the other questions really ask"},
  rtask="The same answer for your second-choice role: which part changes?",
  rkey=[{"t": "Short answer", "l": ["Mostly the last part, and sometimes the story: pick the one that shows what the second role values most."]}])

EXTRA["C12"] = dict(
  teach="Each usual interview question asks something else. ‘Why here?’ asks how much research you did. ‘Your weakness?’ wants a real one and what you’re doing about it. ‘Why you?’ means why you over the other five. For a challenge or a conflict, tell it as STAR: situation, task, action, result. You’re not there to be judged, but to offer what you have.",
  walk=[{"h": "The translations", "l": [["Why here?", "From their mission, clients and values, not the pay or perks."], ["Your weakness?", "A real one, ideally not central to the role, and what you’re doing about it."],
                                         ["What makes you unique?", "A rare pairing, such as numbers plus people skills."], ["Career plans?", "How long you’ll stay, and whether you’ll grow here."]]},
        {"h": "STAR", "l": [["Situation.", "Where and when, in one line."], ["Task.", "What you had to do."], ["Action.", "What you did, in the first person."], ["Result.", "What changed, with a number if you have one."]]},
        {"h": "Offer, don’t audition", "p": ["Dr. K’s mindset: you’re not there to be judged; you’re there to offer what you have and let them decide whether it fits. It takes the fear out of the room."]},
        {"h": "Where it goes wrong", "l": ["‘Why here?’ answered with the salary.", "‘I’m a perfectionist.’", "A STAR story with no result."]},
        {"h": "Worked: a STAR answer", "p": ["Situation: a group project with a team member who stopped replying two weeks before the deadline. Task: deliver the report anyway. Action: I split their part among us, messaged them once with the new plan and a clear ask, and told the teacher early. Result: we handed it in on time with a 7.5, and they rejoined for the presentation."]},
        {"h": "Your turn: one employer", "p": ["For one real employer in your top role: why here, your real weakness and what you’re doing, your pairing, and one STAR story."]}],
  key=[{"t": "A good answer looks like", "l": ["‘Why here’ built from two facts on their site.", "A weakness that’s real, with a step you’re already taking.", "A pairing no generic candidate would claim.", "A STAR story ending in a result."]}],
  thread={"b": "C11 · your opening answer", "n": "C13 · the rounds, from their side"},
  rtask="The same four answers for an employer in your second-choice role.",
  rkey=[{"t": "Short answer", "l": ["‘Why here’ changes completely, the weakness and the STAR story usually stay, and the pairing shifts to what that role values."]}])

EXTRA["C13"] = dict(
  teach="Many employers hire in three rounds: the hiring manager checks your history and values, a skills round tests real work, and a last conversation checks fit, sometimes by telling you the hard parts. Knowing them tells you what to bring: proof you can show, an assignment treated as the job itself, and your own questions.",
  walk=[{"h": "Three rounds", "l": [["History and values.", "The hiring manager, with your CV."], ["Skills.", "Often future colleagues: real scenarios, your portfolio, an assignment. Whatever you show here is taken as your best."],
                                     ["Fit.", "Whether the job is right for you too; they may describe the hard parts to see how you react."]]},
        {"h": "Bring proof", "p": ["One piece of work you can walk through in three minutes beats a list of skills. If they set an assignment, do it as if it were the job."]},
        {"h": "Your questions", "l": ["A line from the ad: what does it look like in practice?", "How would I exceed your expectations?", "What do the first 30, 60 and 90 days look like?", "How do new people learn here?"]},
        {"h": "Where it goes wrong", "l": ["Treating the assignment as homework.", "No questions of your own.", "Talking about tools instead of what the work changed."]},
        {"h": "Worked: three minutes on one project", "l": [["The problem.", "A wholesaler’s on-time delivery fell in the second half of the year."], ["The data and method.", "Two years of order lines, cleaned and modelled in Power BI."],
                                                            ["What you found.", "One warehouse’s switch to a cheaper carrier, with both sides priced."], ["What you’d do next.", "Find out what a failed delivery really costs."]]},
        {"h": "Your turn: the skills round", "p": ["The one piece of work you’d show for your top role, its three-minute walk-through, and your five questions."]}],
  key=[{"t": "A good answer looks like", "l": ["One project, told as problem, method, finding, next step.", "Three minutes, timed.", "Five questions, one about how new people learn.", "A plan for an assignment: ask what good looks like, then deliver a bit more."]}],
  thread={"b": "C10 · where you’re applying", "n": "C14 · the pay question"},
  rtask="The piece of work you’d show for your second-choice role: the same one, or another?",
  rkey=[{"t": "Short answer", "l": ["Often the same project, told with a different emphasis: the method for an analyst role, the advice for a consultant role."]}])

EXTRA["C14"] = dict(
  teach="Research pay before anyone asks. Give a range from real sources with your target in the upper half; a number far above the market hurts you, a reasoned range shows you think. In the Netherlands compare packages, not monthly pay: at least 8% holiday pay by law, and a CAO may add a 13th month and a pension.",
  walk=[{"h": "Research first", "l": ["Ads that give pay.", "The CAO scale, if the sector has one.", "Salary sites.", "What alumni and people in the role told you."]},
        {"h": "A range, not a number", "p": ["Leila Hormozi’s advice: give a range with your target in the upper half, and say where it comes from. It shows you’ve done the work, and leaves room to agree."]},
        {"h": "The Dutch package", "l": [["Holiday pay.", "At least 8% of your gross yearly salary, by law."], ["A 13th month.", "In some CAOs and companies."], ["Pension.", "Often part of the CAO."],
                                          ["Probation.", "None on contracts of six months or less; at most one month up to two years; at most two months on longer or permanent ones."],
                                          ["Pay transparency.", "A law aimed at 1 January 2027, not yet passed: employers would have to give the starting pay or range, and couldn’t ask what you earn now."]]},
        {"h": "Where it goes wrong", "l": ["Naming a number with no research behind it.", "Mixing up gross and net.", "Forgetting holiday pay when comparing two offers."]},
        at({"h": "Worked: a starter’s range, November 2026", "p": ["Two ads for junior supply chain consultants gave pay: %s a month on a traineeship, and %s–%s. A range of %s low, %s target, %s high. The target over a year: %s × 12 = %s, plus 8%% holiday pay (%s) = %s. With a 13th month, %s." % (eur(PAY_RANDSTAD), eur(PAY_LEVVL_LO), eur(PAY_LEVVL_HI), eur(LOW), eur(TARGET), eur(HIGH), eur(TARGET), eur(YEAR), eur(HOLIDAY), eur(YEAR_H), eur(YEAR_13))]}, LEVVL),
        {"h": "Your turn: your range", "p": ["Your range for your top role from at least five sources, as gross monthly low, target and high, and the yearly package."]}],
  need=[{"k": "Ads with pay", "v": "%s a month · %s–%s" % (eur(PAY_RANDSTAD), eur(PAY_LEVVL_LO), eur(PAY_LEVVL_HI)), "n": "junior supply chain consultant, November 2026"},
        {"k": "Holiday pay", "v": "at least 8%", "n": "of gross yearly salary, by law"}],
  key=[{"t": "Worked answer", "l": ["From the example: %s low, %s target, %s high a month." % (eur(LOW), eur(TARGET), eur(HIGH)),
        "The target as a package: %s a year, plus %s holiday pay = %s; %s with a 13th month." % (eur(YEAR), eur(HOLIDAY), eur(YEAR_H), eur(YEAR_13)),
        "What to say: ‘From the ads and the people I spoke to, roles like this pay about %s to %s a month. I’m aiming for around %s, depending on the whole package.’" % (eur(LOW), eur(HIGH), eur(TARGET))]}],
  thread={"b": "C12 · the questions behind the questions", "n": "C15 · raises that follow what you do"},
  rtask="Your range for your second-choice role, from at least three sources, and the yearly package.",
  rkey=[{"t": "Short answer", "l": ["Low, target and high a month, each from a source; the yearly figure with 8% holiday pay. If the two roles pay very differently, that belongs in your choice too."]}])

EXTRA["C15"] = dict(
  teach="Raises follow value, and value counts only when someone sees it. Switch from doing the work to showing it: a short weekly note on what you did and what it changed. Plan where your part of the work should be in a year, manage your own time well, and once a year check your pay against the market, with your evidence.",
  walk=[{"h": "Show the work", "p": ["Leila Hormozi’s first habit for promotion: switch from executing to advocating. A weekly note to your manager: three things you did, and what each changed."]},
        {"h": "Plan for tomorrow", "p": ["Write where your part of the work should be in a year, and what it needs. Managers promote people who think about next year, not only this week."]},
        {"h": "Your own time first", "p": ["Manage your own time well before you ask to manage others: it’s the first thing a manager checks."]},
        {"h": "Once a year, the market", "p": ["Pay should track fair market value for your skills, not one busy month. Once a year, check the market with the sources from your range, bring your results, and name the number. Dr. K mentions research suggesting that people who move jobs every two to five years earn the most, though it depends on the field."]},
        {"h": "Where it goes wrong", "l": ["Waiting to be noticed.", "Asking for a raise after one busy month.", "Threatening to leave as a tactic."]},
        {"h": "Worked: a weekly note", "l": ["Rebuilt the stock report so it updates itself: saves the team about an hour a week.", "Found that two suppliers deliver late most weeks; sent the planner the dates.", "Next week: the order-error list, so we can fix the top three at the source."]},
        {"h": "Your turn: your first note", "p": ["Your first weekly note, and a yearly date to check your pay, with what you’ll bring."]}],
  key=[{"t": "A good answer looks like", "l": ["Three lines, each a thing done and what it changed.", "One line on next week.", "A yearly date in the calendar, with the sources you’ll use and the results you’ll bring.", "Your rule for when you’d change jobs rather than ask."]}],
  thread={"b": "C13 · showing your work in an interview; C14 · your range", "n": "the ten applications, and then the job"},
  rtask="Write the weekly note for your internship now: three things from this week, and what each changed.",
  rkey=[{"t": "Short answer", "l": ["If you can’t name what changed, that’s the finding: ask your supervisor this week which of your tasks matters most, and start there."]}])

GLOSSARY = [(3, "CAO", r"(?-i:\bCAO\b)"), (9, "FORD", r"(?-i:\bFORD\b)"), (12, "STAR", r"(?-i:\bSTAR\b)"),
            (14, "holiday pay", r"holiday pay|vakantiegeld"), (14, "probation", r"probation|proeftijd")]

def check():
    assert (LOW, TARGET, HIGH) == (2800, 3200, 3500) and YEAR == 38400 and HOLIDAY == 3072 and YEAR_H == 41472 and YEAR_13 == 44672
    assert PAY_LEVVL_LO <= LOW <= PAY_RANDSTAD <= TARGET <= HIGH <= PAY_LEVVL_HI
    for x in L:
        x.update(EXTRA[x["id"]])
        assert len(x["teach"].split()) < 75, (x["id"], len(x["teach"].split()))
        assert x["walk"][-1]["h"].startswith("Your turn") and len(x["walk"]) >= 4, x["id"]
        for where, t in lesson_texts(x) + [("rtask", x["rtask"])] + [("rkey", q) for b in x["rkey"] for q in b["l"]]:
            assert not re.search(r"\b(he|him|his|himself|she|her|hers|herself)\b", t, re.I), (x["id"], where, "pronoun", t)
            if where != "thread":
                assert not re.search(r"\bC\d\d\b", t), (x["id"], where, "points at another lesson", t)
            assert not re.search(r"%%|%[sd]\b", t), (x["id"], where, "format left over", t)
check()

C = course({"goal_id": "goal_career", "key": "career", "title": "From graduate to hired", "azTitle": "From graduate to hired, A → Z",
     "rungs": ["Aim", "Prove", "Show", "Reach", "Interview", "Pay"],
     "rungDesc": ["list every option, choose on purpose, and read ten ads", "close the gap the ads show, results with numbers, and feedback",
                  "a CV that reads as an advert, and a LinkedIn that says it first", "conversations with people in the role, and applying up",
                  "your pitch, what the questions really ask, and the three rounds", "a researched range under Dutch rules, and raises that follow value"],
     "blurb": "One question on your own career per sitting, mostly on the role you’re aiming at after graduating, with the revisit on your second choice. The worked examples use real Dutch vacancies for junior supply-chain roles, as checked in November 2026. Written in my words from Leila Hormozi, Dr. K (HealthyGamerGG), Vinh Giang, Justin Sung and Alex Hormozi in your library; the Dutch pay and contract rules were checked in November 2026.",
     "allDone": "now send the ten applications. 🎓",
     "revWord": "another role",
     "refNote": "The idea opens in step 2 of the sitting — guess first. The videos are for when you want more; the Dutch rules were checked in November 2026, and the pay-transparency law isn’t passed yet."}, L)
check_videos(C)
check_extras(C["lessons"])
FLAGS = term_order(C["lessons"], GLOSSARY, "C")
if FLAGS:
    sys.exit("A lesson uses a term before the lesson that teaches it, with no pointer:\n  " + "\n  ".join(FLAGS))
write("CAREER_CURRICULUM", ["From graduate to hired — 15 sittings on the Career goal, in my words from the career videos in the youtube-digest",
      "library (Leila Hormozi, Dr. K of HealthyGamerGG, Vinh Giang, Justin Sung, Alex Hormozi): options, purpose, ten ads, closing a gap,",
      "results with numbers, feedback, the CV and LinkedIn, networking, applying up, the interview questions and rounds, a salary range under",
      "Dutch rules (8% holiday pay, probation, pay transparency) and raises. Built by scripts/build-career-course.py."], C)
