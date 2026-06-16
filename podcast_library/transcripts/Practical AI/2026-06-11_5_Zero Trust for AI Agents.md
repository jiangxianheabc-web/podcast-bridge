# Zero Trust for AI Agents

- **来源**: https://share.transistor.fm/s/5c1a087d
- **节目**: Practical AI
- **时长**: 47:01
- **转录时间**: 2026-06-16 23:36
- **模型**: BcutASR (必剪)

---

## 章节

- **00:01** 平台需要解决发现和增长
- **05:17** Because ai or , uh How shoul...
- **10:41** That , you know , without go...
- **15:53** Which i very much like in ou...
- **21:02** Uh , there's sometimes unsco...
- **26:12** And when we're talking when ...
- **31:29** Web3 提供更直接的价值转化路径
- **36:40** We need to know that this hu...
- **41:42** But then they do provide a k...
- **46:54** But you'll hear from us agai...

---

**[00:01 - 00:29]** welcome to the practical ai podcast where we break down the real world applications of artificial intelligence And how it's shaping the way we live , work and create Our goal is to help make ai technology practical Productive and accessible to everyone Whether you're a developer Business leader or just curious about the tech behind the buzz You're in the right place be sure to connect with us on linkedin x or blue sky To stay up to date with episode drops

**[00:29 - 00:37]** Behind the scenes content and ai insights You can learn more at practical ai dot fm Now on to the show

**[00:41 - 01:08]** Welcome to another practical ai podcast episode This time it's just chris and i michael host In these episodes where it's just the two of us We try to take something that's in the ai news or a topic for a deep dive Something that will help all of us Level up our ai and machine learning game I'm daniel whitneck I'm ceo at prediction guard And i'm joined as always by my cohost chris benson

**[01:08 - 01:35]** It was a principal ai and autonomy research engineer How are you doing , chris Hey , doing great Lots of cool stuff out there Uh , looking forward to today's conversation Yes Yeah , for sure . there's There's no shortage of , of things to talk about But even in our i don't know If you remember this passing comment , chris But i think it was in our episode Where we were talking about mcp on top of cooper netties

**[01:35 - 02:02]** The , the guests , uh , mention that , hey when anthropic kind of drops one of these white papers or research topics or blog post Often that's a window into something that's that's significant and something to pay attention to And , and review in detail And it just so happens that they on may I think twenty seventh of this year Twenty twenty six released this

**[02:02 - 02:32]** I guess it's a ebook white paper block post However , you wanna frame it , uh , framework Uh , around with zero with dust Yeah Zero trust for ai agents We share a security framework for deploying autonomous ai agents in the enterprise Covering the new threat landscape A tier zero trust architecture and defensive operations Built for ai accelerated attacks So that's all that's a lot of words

**[02:32 - 02:59]** Now , i think first off , chris , it's probably worth recognizing that anthropic Obviously has a has a horse in this race especially with things like cloud Code or cloud code work or all the cloud things These are autonomous agents that can operate in your enterprise environment So obviously i think probably there are things that are happening And things where their customers or people using these tools are obviously

**[02:59 - 03:28]** Thinking about the security implications of that They also recently released cloud security Which is more on the ai for security side Not so much the security for ai side Which is mostly what we'll talk about today in relation to this To this article or , or ebook But yeah I i think that's worth acknowledging Obviously if people people have a secure way of deploying autonomous agents

**[03:28 - 03:57]** I'm sure they are hoping that many of those are built on anthropic technologies I'm sure they do And , and , you know , just to keep in the back of our mind Uh , this is the same organization that has methos out there and is working with I believe the latest number is one hundred and fifty organizations is the latest thing I saw published , um , on their website Uh Trying to go through and do security audits and such as that And , um , with the timing of this I would guess don't know

**[03:57 - 04:23]** But just making a guess that , um Some of the , uh , leveling up that methos has enabled , um Is probably driving some of their zero trust and , and other security Uh , concerns going forward So , uh , looking forward to this Yeah Uh , yeah I guess that's a good place to start with the kind of premise of this I think there's a few things to frame here Maybe one is there is probably a segment of the market

**[04:23 - 04:50]** And of our audience that is already using autonomous agents for something Even if that's just like cloud code or Or something like that for development purposes Where by autonomous i mean it's making actions on On your behalf to do some things And , and i think generally in terms of where we're seeing the market going on the positive side And organizations are going to need to more

**[04:50 - 05:17]** and more adopt these autonomous agents within their organization for value Creation or new revenue or opuh You know , saving on operational efficiencies So that's like thing You know , premise one is that that's the way the markets going I think the , the other kind of background to this Though is like you were saying There's a bit of a forcing function here

**[05:17 - 05:46]** Because ai or , uh How should i , so attackers So malicious parties Hackers , et cetera , have equal operate You know , they have equal access to these agenic coding and development capabilities themselves , right meaning that the pace at which people are about to be Or already being attacked and exposed to threats in their infrastructure is just like , uh Expanding exponentially

**[05:46 - 06:15]** Which means you cannot keep up with the That level of attack using human only approaches Meaning that the forcing function that i'm talking about is you are necessarily going to have to adopt autonomous agents At least to help you manage the threats associated with With the offensive use of this ai technology So i think there's the , the positive side of this , obviously Which is we there's , there's a future Where autonomous agents are doing very positive things

**[06:15 - 06:44]** And you have this kind of digital workforce of agents within your organization But the maybe part of the forcing function behind this discussion is that people actually need to adopt autonomous agents Because of this offensive threat to their infrastructure Yeah I , i agree And i think that'll put that'll put quite a strain on a lot of the , the humans involved Uh , in this Because , um , you know , there's , there's a certain amount of leveling up from a human standpoint to understand

**[06:45 - 07:14]** Um , um , what , uh What different harnesses are and what the different capabilities that are now becoming available , um Understanding different vendors versus open source and such as that Um So to actually get to the point where you can start implementing these Um , is a bit of a lift And i think that that's going to be something that we observe is that i think there'll be a spread across organizations Where you'll have some You know , the , the end You know , on one extreme And you have the anthropics , uh That are , that are leading the way

**[07:14 - 07:44]** And producing these capabilities and stuff like that But then there's a lot of kind of a mom and pop , uh , organizations Or maybe not that small But , you know , mid size and stuff like that They were gonna struggle to level up just a little bit And so i think we have some interesting I think the security landscape will be , uh Very interesting a little bit wild west Uh , in the days ahead Um , as people , even if tools are available They have to get to where they can uptake those , um And , and get productive with them

**[07:44 - 08:13]** So i , yeah Yeah So i , i , i agree And i think the us or , uh Maybe a way to get into this discussion is that if we frame the background with an assumption , uh And i'm sure there are arguments against against this assumption But let's assume that your organization is And will adopt autonomous agents for You know , positive things Like i talked about operational efficiencies New , new revenue Whatever that is , and , or

**[08:14 - 08:44]** Uh , cyber security purposes If we assume that , then you say , well Okay Well now we're gonna have these autonomous agents operating in our environment They could cause all sorts of harm themselves so it's like i could shoot myself in the foot Trying to protect against the offensive malicious people by releasing a bunch of agents into my infrastructure And they themselves cause a lot of , a lot of harm Like how do i how do i manage those things ? and anthropic has

**[08:45 - 09:15]** So they , they have not come up with this idea of zero trust To be clear This is a general concept We which we could talk about the definition of but they're essentially releasing with this framework a way to think about a zero trust approach Or a zero trust framework for managing ai agents or autonomous agents within your organization So maybe , maybe it'd be good to just define that Define that term first in the , in the past

**[09:16 - 09:43]** Uh , if we , uh If , if we think about cyber security There's been what's generally referred to as parameter based cyber security This is , uh , more traditional model that would focus on that boundary of your organization And outside or internal and external And the the kind of core principal being that i'm gonna trust everything that's inside And distrust everything that's on the outside

**[09:43 - 10:13]** So there is a parameter in which within that parameter i trust things A zero trust approach to cyber security , on the other hand Would actually assume that And everything inside the network , uh Uh , uh , uh , that , that threats are already inside your network Already inside your parameter So it treats every user device request as a potential threat So that that's why it's called zero threat

**[10:13 - 10:41]** And the like i say , this has been something that's been around from for a long time Nist has published about it Uh , in zero trust architecture back in twenty twenty And other government organizations and others have have talked about it as well So that's that kind of that kind of difference I don't know if , if those if If that zero trust idea has crossed into your Your parameter of knowledge Chris , i'm sure yes

**[10:41 - 11:11]** That , you know , without going into any detail at all Working in defense and intelligence that , uh It , it is pretty core Um And yeah I mean , i mean But , uh , the simple way of thinking about is every single api request Uh , that you have Uh , has to have security credential , uh And that can be from a variety of Of different , uh , mechanisms But , um You don't trust anything And everything is down to a granular level Unless it , it , it is authenticated and authorized to do whatever it is trying to do

**[11:11 - 11:37]** So , um And the world that i'm living that's pretty standard , um Though i think as , um I think , i think there's room for all of us Uh , even those of us who have been doing it to level up and get better at this So i don't think that there's anybody Who has has just nailed it So it's it's one of those One of those ongoing learning curves Yeah And , and we're we're about to dig into a lot of that as related to ai agents

**[11:37 - 12:03]** however , to your point there's a lot of organizations that are still trying to think about this concept Even generally in their kind of general cyber security world And , uh You know , one of my One of my hot takes here is Is we'll talk about that the these kind of foundational things that anthropic is suggesting And you know , probably ninety percent of plus of of organizations

**[12:03 - 12:32]** Enterprises that have ai deployments currently are not operating according to this model They are according to this framework They would be completely exposed And i think so just acknowledging Much of this is probably aspirational for enterprises And they need to work towards it in a maybe a more rapid way Just because of how things are advancing And you know , there's better tooling out there day by day Better products , et cetera But yeah

**[12:32 - 13:00]** This is just just so if you're out there And you're thinking i have agents running And i have none of what we're about to talk about That's probably the situation that most are in , in In the enterprise world would be hopefully today We can , we can help people start on a , on a path here Yeah Exactly Next week you have no excuse But coming into this conversation You , you have an excuse Ha ha ha U

**[13:02 - 13:31]** Um So i , i think the i would encourage people If you just search for zero trust for ai agents You know , anthropic blog post will link it in the show notes as well So you can click through to that ebook And the framework itself there's a lot that we won't be able to cover in detail But i think the overall structure that they present our sum Some kind of initial background and considerations Kind of definitions related to autonomous systems that that people need to consider

**[13:31 - 13:59]** And , uh , then they talk about the current threats to those aggentic or autonomous systems And then how to apply the zero trust to those threatened agent tic systems That's kind of the the flow of Of , of what they talk about So the , the first thing And i think this is something we've talked about more on the show And have have already covered But just to set the foundation Some of these considerations

**[13:59 - 14:28]** Kind of background information that That we may want to give is that , you know , why Why are we talking about like a new framework While agents are different and how they operate We've talked about this on the show before they use a distributed set of tool They interpret instructions Try to accomplish goals They execute operations without human initiation Think importantly , uh , they might preserve context across sessions if they're trying to accomplish some goal

**[14:28 - 14:57]** And then you kind of add multiple agents And they might communicate with one another So you've got this multi agent communication Now there's a couple terms here Chris , that i think we've even mentioned But they just defined specifically Uh , related to agent security Uh , um , as new terms of people might Might be , uh , unfamiliar with One is blast radius Which , uh , kind of , i think people could assume what that means , right

**[14:57 - 15:24]** It measures the potential damage if something goes wr If an agent does , does go off the rails of that blast radius and least agency Which i guess is a term coined by oasis And , and that extends this kind of idea of least privilege to aggentic application So you shouldn't be giving more agency to your agents than they need to do their agent things And that's standard zero trust ideas

**[15:24 - 15:53]** You , you , you give it just what it needs and absolutely no more So yep And , and so that's kind of the I guess the background in which in which we're operating Then then the anthropic paper goes into these current threats Which is some are ones we've talked about Some are ones we've not talked about as much , chris , um It's interesting that they talk They kind of frame everything within the agent world as aggentic systems

**[15:53 - 16:22]** Which i very much like in our , in our product That's why i insist on using the idea of ai system as , as a thing Because you have these distributed set of things that are powering agents these days And so they kind of break down Then this like current threats to agent ententic systems The first of those Which is probably not a surprise because it's the first on owasp list Often as well is prompt injection and instruction manipulation

**[16:22 - 16:49]** Um we've again , we've talked about this There's everything from the obvious direct You know , human input into a chat on her face Ignore your instructions and do this other thing Which you shouldn't be doing But the one that they mention as the more , uh did difficult or scary one would be the indirect prompt injection Where that's coming in through Maybe it's a file that's

**[16:49 - 17:18]** You know , you have an agent connected to your email And , uh , attachment comes through with hidden instructions in it Um Yeah Anecdotally I , i helped another company do some interviews And i , i wrote a technical exercise and put it in a pdf And i knew everyone would use cloud code like they should But just , just because i wanted to be fun I , i had all the instructions in black text

**[17:18 - 17:45]** And then i had an extra like three force of a page So i just filled up that page with , uh with instructions that would make cloud code Do the opposite of what i was saying in the instructions , um Just to , just to see if they would catch it Um So that that sort of thing very devious Very devious It was , it was that did you make it white text in the pdf Yeah It wasn't obvious Just like white space on which Which would get interpreted

**[17:45 - 18:14]** If you just uploaded it a cloud code or , or whatever That's u very sneaky But actually quite common in terms of vector I mean Because everyone just throws everything they can , uh You know , the way , the way things have been operating And so Yeah , that's what we're doing today Ha ha ha Yes True Um and i guess the other So that , that , that's threat number one Prompt injection instruction manipulation

**[18:14 - 18:42]** Threat number two , that they talk about Which is related to agents using tools Uh , particularly through mcp Which was a topic on a recent comm or recent episode of this show Which you can look back at for For much more information on that on mcp Yep On mcp Yeah so they talk about agents that can manipulate tools Maliciously or kind of do things that they shouldn't be doing because of privileges

**[18:42 - 19:11]** I i think about chris like it It's kind of like you set up a server uh , maybe i set up a fast api Api that , you know , my agent could use And i only tell it about instructions you know , about a couple Get , get routes on the api in the instructions But i don't shut down the other routes , right And if the agent was smart in any sort of way Right

**[19:11 - 19:38]** It could just look at the swagger Documentation at the slash docks in point And know about all the other routes that maybe it shouldn't use And then like all of a sudden i have problems , right That's right Yeah And just to clarify , swaggers a protocol that that defines what those routes are Um , and , and , you know , you mentioned You know , kind of going off the rails But , um , you know , the , the notion of my , uh Mh malicious mcp server has now been documented , uh

**[19:38 - 20:07]** And there could be lots of various types of tooling Um , that is coming into being now Just to take advantage of these vulnerabilities So , um I think you'll , we'll see a whole class of malicious software arising , um To , to do these kinds of , uh , of tool and resource this use And yeah Yeah Exactly And , and a lot of times These tool descriptors or schemas or metadata is injected into the context for an lm

**[20:07 - 20:36]** You actually generate the output So if i'm a malicious party Or maybe just an agent that doesn't know what it's doing and and like they say it's drifted from its goals or something There's nothing preventing that from doing this poisoning thing Where i like find out about the descriptor schema and metadata And i even modify that in the instructions to Maybe get the mcp server to do different things , right So this , this tool and resource misuse is definitely , um

**[20:36 - 21:02]** It is a reason why it's kind of number number two there Um The , the next one Uh , identity and privilege abuse So yes Yes Exactly So , um , they talk about this Agents often operate with elevated privileges or service accounts And traditional identity systems designed for humans struggle to accommodate them

**[21:02 - 21:29]** Uh , there's sometimes unscoped privilege inheritance Um , almost like i , i , i kind of think about this like , um What was , uh Uh That , uh , that cyber security book from , uh , it's like the cuckos Oh yes The cookies nest or something That was great Someone can tell us in , in the comments But it's like you You kind of land one place in a network And then you escalate privileges , right

**[21:29 - 21:59]** And you can move laterally and go in all of these directions , right Really old book It was one of the original cyber security books that came out before It was really a field Um I read it many years ago And yeah , definitely inspiring Yeah And so goose egg that's that's what it was And as you , uh As you are looking at lots of different agents That have different levels of privilege and different capabilities , um And as agents are formulating things

**[21:59 - 22:24]** You know , right in a , in , in , during run time Essentially , um , that that didn't exist as a preset Static thing that you want to do , uh And they developing that it's very easy for one agent to spin off another agent and get And it has more privilege than it needs And then that can be taken advantage of So there are lots of different variations of , of how those kinds Yeah Yeah , for sure So that's the privilege

**[22:24 - 22:53]** And i should say i , i do really encourage people to take a read through the , the ebook Obviously were highlighting some of these things But there's much more detail there Also a great resource around this If you're trying to learn some of this is if you go to the owsj ai project We've , we've had reps on our show before and , um My teams involved in the ai bomb project And other things with oos there's a lot of great people involved but they have so many great resources online

**[22:53 - 23:20]** Related to this sort of thing And , uh , guides for mcp Guides for agent entic security , et cetera So take a look at those as well You might be listening to this episode and thinking that , hey I and part of one of those organizations that's in the ninety percent of enterprises That are not ready security wi For autonomous agents operating in my environment

**[23:20 - 23:50]** How am i gonna manage supply chain risks And have an ai build materials and define agent boundaries Secure tool access and implement input validation and output controls Well this is one of the reasons Why i think it's so important to have great platforms that don't Require you to build your own ai Agent governance platform That's why outside of the practical ai podcast

**[23:50 - 24:18]** I personally am leading an organization full of really smart people that are thinking about these problems And have brought prediction guard Uh , into , into existence Prediction guard is an ai control plane that self hosted It lives in your own infrastructure where you're gonna deploy those autonomous agents And it allows you to manage this supply chain risk and put in governance Policies that are enforced and maintain observability over those agents

**[24:18 - 24:42]** And i'm just really excited about the capabilities That are that that are already in the product And are being released later this year So i would encourage you Please check us out at prediction guard dot com slash practical ai you can book a call with me and the team to discuss How so you're going to manage security for your agents operating in your enterprise

**[24:46 - 25:15]** prediction guard dot com slash practical ai The next one that anthropic highlights is supply chain and dependency risks Uh huh So , uh , you , you were just mentioning How sometimes agents compose things at run time Chris This includes potentially loading external tools or installing packages or changing infrastructure And so that , that , that supply chain can actually update in

**[25:15 - 25:45]** In real time or at run time As agents are trying to accomplish a task But also model on tool , uh , supply chains So models have their own supply chains related to the weights And how they were trained or fine tuned , um How , how easy it is to jail break them or prompt inject them But then mcp servers are also software components , right They have their own integrations They their own software dependencies , et cetera Which have their own potential vulnerabilities

**[25:45 - 26:12]** Um So all of this it's It's very much a multi layered thing that it is could evolve dynamically Which is kind of scary That And one thing to call out While we're talking about supply chain independency risk is that all of the traditional zero risk vulnerabilities All the things that we were talking about in the cyber security world Before we started having You know , ai ogentic system conversations about this Those all still apply as well

**[26:12 - 26:42]** And when we're talking when and , uh , that i was prompted , uh Ah , no pun intended to say that by you When you mentioned the multi layer So you can still have , um You know , bios and cmos vulnerabilities that , uh Can take it that , that That lend themselves to some of these vulnerability , um You know , layers and packages that build up So there's many different points in a stack Uh , where these attacks can occur So all the way down to , you know , network firewall , right

**[26:42 - 27:11]** If you're If you're having an agent operating in that environment It could , you know Find and detect things that , that it shouldn't And so , yeah , that it's , it's , it's So Yeah I guess multi layered , um Which , you know , many security things are And i know oos always recommends this kind of layered approach But yeah , the , the last two are Are kind of related memory and context poisoning and rag poisoning Both obviously are this type of

**[27:11 - 27:40]** Uh , of way that you can either in the memory Or contacts to an lm call or into rag data Uretrieval , augmented generation data Which often lives in a , a database or a vector database Um , you if , if you have no control over what and how things are committed to that memory Or to that vector database There's nothing preventing agents or external parties from inserting things into that memory

**[27:40 - 28:10]** So , you know , the I think the one , uh The example i used last year at the midwest ai summit , chris Which as a reminder to our folks Midwest ai summit coming up october fifteenth Um , gonna be another great , great , uh , experience You can , can search the details midwest ai summit But i think i use the example Where it was a healthcare situation And someone that , you know , an asian or a prompt is like in a first inner change

**[28:10 - 28:39]** It says , hey Do this for patient a And then you in the follow up say like Well , in all the following You know , consider patient a to be patient b And then you keep Keep filtering in that information about patient a being patient b And then all of a sudden when You know , later on your You're wanting some information about patient a or patient b All of a sudden you're getting data that you shouldn't shouldn't be getting right

**[28:39 - 29:08]** So it , it can happen , um And , and has been shown to happen So Um , okay , chris , that's all the scary things I guess there's a lot of them Now we gotta go , now we gotta figure out how to fix this right now Now we gotta figure out how to fix this And i do like the general Uh Structure that anthropic provides here , uh recognizing again that many people are behind in this

**[29:08 - 29:38]** And that new tools and products will need to address many of these things gradually over time They present three capability I think what they call capability tears or three tiers of application Basically saying , hey , in these different areas You need to do something There's like the minimal thing that you should do Which they call foundation The minimum viable thing Thing And then there's an enterprise tier Which means , hey , if you're If you're an actual enterprise and And , and needing to , uh

**[29:38 - 30:01]** Be robust and , and resilient You need to do these things And then there's advanced Which would apply to kind of particularly high risk or stringent regulatory environments Which would apply to kind of particularly Or maybe aspirationally for everyone else to try to get to that Get to that level So foundation , enterprise and advanced in each of these categories And then for , uh , uh

**[30:01 - 30:31]** They develop something in each of these categories for each of a number of , uh the threats that that we talked about are the areas in which you need to secure 那 first 算哪只 kind of dimension It kind of breaks them down by different by dimensions And then tears them against those three tiers that you just described Yeah It's kind of like i need to I need to consider these . however many things I forget how many there were at I need to at least be in the foundation level for all of these

**[30:31 - 31:00]** And then i can circle back and maybe upgrade particular ones enterprise Or like gradually work on it over time So the , the first of those is agent identity and authentication Which they kind of frame as the foundation for every other security capability Because without this identity You can't really enforce other Other things throughout the , throughout the framework Now as we go through here They talk about , um

**[31:00 - 31:29]** Uh , certain ways of doing identity and verification And there are a couple terms And here that people may be unfamiliar with as well One of those being they talk about hardware bound credentials Have have you , uh I'm i'm sure this is also a part of , of your life over time Chris a hardware bound credentials Or where you have to present Uh , of , you know , you may be ua usb or something You know , there's a lot of different ways It can , it can

**[31:29 - 31:59]** But you have to insert a piece of hardware Or make act and make accessible a piece of hardware Which provides that authentication in which an adversary would be unlikely to have in their possession And that doesn't necessarily do it by itself Uh , it's there's usually multiple tears But , um , that's that is one way of , uh Of contributing significantly is if you don't have a physical piece of hardwin your hand You're not gonna be able to Uh , to gain access Even if you can break through other tears So , yeah

**[31:59 - 32:25]** And this idea of it being bound to hardware I think is the key The key point that that you're referencing chris where Uh , otherwise they view kind of , hey If you have api keys , for example And those are just floating around You should probably consider those already compromised if we're going with this idea of zero trust versus If an agent has an identity

**[32:25 - 32:55]** And has an authentication to access this environment It has authentication tied specifically to the hardware that it's operating on You know , something like that , that hardware bound credential is , is something that they talk about And just to give some examples here in the agents Agent identity and authentication piece the foundational And we won't be able to go through all the tears of all the categories

**[32:55 - 33:21]** We just don't have time But just to give an example of , of these Uh , there is , um The agent identity , identity verification piece The foundation level that they suggest there's to have unique cryptic graphic Identifiers for each agent instance So to assign persistent agent ds backed by cryptographic material

**[33:21 - 33:49]** Not just labels the track agent life cycle from creation to retirement ideas appear in all logs and access requests The enterprise level is certificate based authentication with full lifecycle management And the advanced is hardware backed identity with attestation So that advanced , you know , you store agent credentials in hardware Security modules or trusted platform modules Right

**[33:49 - 34:18]** With remote at test station Which there's a whole rabbit hole You could go down there with those with those terms But that would fit into their Into their advanced category . that's right Yeah Um So that's , that's an example of one of these categories , agent identity and authentication The next , uh , category that they That they talk about is access control and privilege management So assuming you have an identity for your agent

**[34:18 - 34:47]** Then you need to control access and privileges for that agent And , uh And that authorization layer should enforce this idea that We defined earlier of least agency Which is ensuring agents receive only the access Required for their specific function And this can get very subtle Like that api example that i gave You could only tell an agent about these endpoints

**[34:47 - 35:15]** But if you haven't physically , like if you haven't literally shut off the network for other end points or something Um Then there's nothing preventing that agent from like going off of the Off of the rails in that case So , yeah Just to give another kind of set of examples here access control foundation level is role based Access control or r back with denied by default That's the , the foundation and in that category that's , right

**[35:16 - 35:46]** And , and by the way Just as we're working through this wanted to make one quick comment These are all standard zero trust concepts So those of you who in the You know , who may be watching , um You may recognize a lot of these categories and stuff And i think , i think the key is kind of thinking about it within this sogentic context And , um , you know , as , as , as we were all on boarding agents and stuff that that throws it out But keep , keep going I just wanted to call that out for those that might recognize that Yeah Yeah , for sure Um

**[35:46 - 36:13]** I think we can't abandon our good security intuition And especially when you start create treating these agents as having an identity and being Uh Operating in the zero trust environment Some of these things kind of flow through If you , if you work out those details But Um , yeah The next , the next category , behavioral monitoring and response Uh , or , uh , sorry

**[36:13 - 36:40]** Observability and auditing , that was , that was , uh So there's , there's actually these two are tied together We could probably talk about them together there's observability Which essentially captures what agents do So it observes what agents are doing And you need visibility into that So you need logging and audit trails Often in our implementations with customers In my day to day work I often like to say , hey

**[36:40 - 37:06]** We need to know that this human user Using this api key triggered this agent Which has this identity to do this goal Which issued these prompts Which triggered this tool call Which had this input Which was blocked by this governance policy , et cetera Like that's where we're You know , and down the line We need that kind of traceability and , and logging

**[37:06 - 37:35]** Otherwise you , you can't have visibility or build rules or monitor things So that's the observability piece But observability captures only what agents do The behavior , behavioral monitoring that they're talking about determines Whether the actions that agents are doing Should be allowed or sususpicious Are they appropriate for what you would expect Are they appropriate Yes That's , right Exactly

**[37:35 - 38:04]** And , and this is behavioral monitoring and response , right So in certain cases Like i say , when , when When we enforce governance policies We say , well If we see this Then do this , right Um So sometimes that's blocking certain things Sometimes it's just logging Sometimes it's a , you know , alerting someone using a , a particular platform Okay The , the last , uh Second to the last one is

**[38:04 - 38:29]** Is input validation and output controls I think actually this one So what are we on ? one , two , three , four This is the fifth one This is probably the one that most often comes to people's mind And i think is often maybe over emphasized , uh Which is this idea that you would have point checks over You know , harmful things that the agent could produce in its output

**[38:29 - 38:57]** Or harmful things that could go into the agents context or something This is , uh , very important I would say But it's kind of like table stakes The , the example i usually give is You know , is it bad for me to take my temperature If i want to be a healthy human Well It's not a bad thing You know , you can take your temperature It doesn't mean that you are plugged into a healthy life style Or being governed by a

**[38:57 - 39:22]** You know , health records and as part of a healthcare system And have a primary physician and have a care plan and a diet And , uh , it's just a very limited way to view , um That kind of overall health And if we extend that here This would be these sort of point checks of validating inputs and outputs Which are , yeah , again I would say those are table stakes And the last one is integrity and recovery So

**[39:23 - 39:50]** Uh , uh , all of this prevention and detection assumes agents operate correctly You know , when they don't What , what do you do Yeah And , and i think that's actually a pretty big question in the egentic systems world in that , um If you think about You know , going back a couple of points to behavioral monitoring and trying to identify What's appropriate for agents to be doing You know , within all the other security parameters that we've talked about along the way But when , when you

**[39:50 - 40:19]** When you have gotten outside the bounds of what is appropriate Trying to figure out how to roll agents back , um Especially if they're in critical functions can be quite challenging , um Because those critical functions still have to be addressed And so , uh , if a critical function is compromised Uh , by an agent that is intentionally or unintentionally off the rails Then figuring out how do you take a critical system back and get it , um Get it back to a safe place to proceed in

**[40:19 - 40:48]** Whatever is appropriate for that function can be quite challenging And so , um , i've , i've I've have i have spent some time in that , uh , space myself and , um And i think that there's a lot of imagination that has to go into it That maybe wasn't quite as necessary in , um Pre ogentic zero trust models So , uh , just wanted to call that out Yeah They talk about to To give some examples Chris for configuration integrity

**[40:48 - 41:14]** They talk about on the foundational level version controlled agent configurations And the advanced level immutable infrastructure with attest station On the recovery capabilities They talk about at the foundation level documented roll back procedures To your point that having some Having an idea of what you might do is one thing Being able to actually do it is sometimes a challenging thing At the advanced level

**[41:14 - 41:42]** They talk about self healing systems with autumn automatic remediation So , um , yeah Uh , definitely agree Agree with your points there Um I know that we're getting to the close to the end here , chris And just to kind of wrap things Or , or get close to the end here , uh , uh Anthropic does a good job at kind of saying Hey here's all of this stuff and all of these tears and levels and categories , et cetera

**[41:42 - 42:08]** But then they do provide a kind of phase A phase way that you can think about implementing agents Which i think is helpful Um , one identifying requirements to managing supply chain risks And including they talk about ai bomb or ai build materials A defining agent boundaries Defending against prompt injections Securing tool access Protecting agent credentials And then safeguarding agent memory

**[42:08 - 42:37]** And they give some kind of specifications under each of those phases for , for people to To think about Yeah I think , you know As we're , as we're winding up as they address it I know it just a sheer kind of howl How i perceive the , the , you know , uh Kind of establishing the workflow is in the zero trust world that we've been in for , for a number of years It's fairly static , you know , there , there , there's a lot of things And you kind of have to tick them all off , um And a lot of , uh

**[42:37 - 43:07]** It's a very , it's almost a regulatory approach Uh , to system development Um And i think the thing that agga c implementations require is the is trying to anticipate , um An incredibly dynamic , uh , capability that can arise You know , they can kind of an emergent quality Uh , that , that people are doing And i think what anthropic has done for us is given us a way of taking What we already know in a zero trust context And , and , and pointed out

**[43:07 - 43:36]** You know , that within ogc systems These capabilities , um , are , are you It definitely requires a level up to take the same ideas But get them out of that static mindset and moving into a , uh Anticipating dynamic , uh , capabilities from agents and , um I know as we're in both , both in our own jobs and stuff , um That's certainly required us to kind of level up and reconsider , um It's , uh It makes it for a very interesting problem set to address

**[43:36 - 44:02]** Yeah and there's major thought process changes or philosopc philosophical shifts As you mentioning that as practitioners We may have to make they talk in the , in the ebook Uh Anthropic does about this idea of ai vendoring that hey there's these fragile open source projects out here that you might rely on the thing to do might just be to have your agent ic coding system

**[44:02 - 44:29]** Just completely vendor or literally not , not copy But generate a new version of that project that's proprietary to you and under your control and just included in your project Rather than then bringing in a third party dependency So there's like philosophical shifts , uh , like that I do think there's some hard things that we'll still have to wrestle with around I I , i think there's still some of the

**[44:30 - 44:59]** this conclusion that humans are gonna have to make containment Decisions around how to contain these things And whether it be threats in your environment or agents operating in your environment And if things are moving so fast I just think it's gonna be hard for humans to You know If , if something is happening in your infrastructure And exploit timelines go from , you know Months to , to hours to minutes to seconds

**[44:59 - 45:28]** You can't just like rely on waking up the c So in the middle of the night to prove You know , shutting this thing down , right I mean , this , this is , i mean This is a revolution in cyber security U , um , just to , just to put , um A dot , you know , as we're finishing up here , um Every intelligence agency in the world Uh , is , is learning how to , uh Both defend against and exploit these , these , uh These potential vulnerabilities that we're talking about , uh

**[45:28 - 45:56]** As well as criminal organizations of , of all sizes , shapes Uh , on a global scale So this , uh , uh You know , we're , i , i think we're at the very beginning of this journey Um , i think this is a fantastic start Um , to get us thinking I think we're gonna see a lot more tooling and a lot more capabilities , uh Coming out , uh , in the days ahead , uh And it seems to be coming out very quickly Uh Because the threats , uh , have risen very quickly And so i hope folks find this as useful

**[45:56 - 46:21]** As we did in terms of kind of reframing this modern take on cyber Uh , in our , in the sogentic world that we've been talking about nonstop Uh , throughout this , this last year And we'll , we'll , like i say Include the links in the show notes So take a look at those And excited to , excited to keep the conversation going Thanks , thanks for this today , chris Yeah Thanks for taking us through It was a good , good , good Uh , exercise day would do

**[46:26 - 46:54]** All right , that's our show for this week If you haven't checked out our website Head to practical ai dot fm And be sure to connect with us on linkedin x or blue sky You'll see us posting insights related to the latest ai developments And we would love for you to join the conversation Thanks to our partner prediction guard for providing operational support for the show Check them out at prediction guard dot com Also thanks to break master cylinder for the beats and to you for listening That's all for now

**[46:54 - 46:56]** But you'll hear from us again next week
