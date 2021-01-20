import os
import praw
import re
from tinydb import TinyDB, Query
import anim
from collections import Counter
import spaw

streamable_username = os.environ.get("streamable_username")
streamable_password = os.environ.get("streamable_password")

reddit_client_id = os.environ.get("reddit_client_id")
reddit_client_secret = os.environ.get("reddit_client_secret")
reddit_username = os.environ.get("reddit_username")
reddit_password = os.environ.get("reddit_password")

_spaw = spaw.SPAW()
_spaw.auth(streamable_username, streamable_password)

db = TinyDB("db.json")

reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent="/u/objection-bot v0.0",
    username=reddit_username,
    password=reddit_password,
)

subreddits = [
    "politics",
    "videos",
    "politicalcompassmemes",
    "GoldAndBlack",
    "Anarcho_Capitalism",
    "ActualPublicFreakouts",
    "tumblr",
    "SquaredCircle",
    "vegan",
    "chess",
    "anarchychess",
    "latinopeopletwitter",
    "hockey",
    "nba",
    "nfl",
    "4chan",
    "soccer",
    "baseball",
    "manga",
    "competitivetft",
    "Alabama",
    "Birmingham",
    "rocketleague",
    "dogelore",
    "SubredditDrama",
    "Hobbydrama",
    "RPClipsGTA",
    "cooking",
    "sportsbook",
    "mma",
    "turkey",
    "mud",
    "MechanicalKeyboards",
    "SysAdmin",
    "okbuddyretard",
    "SonicTheHedgehog",
    "LegendsOfRuneterra",
    "kappa",
    "brasil",
    "genzedong",
    "vexillology",
    "dndmemes",
    "saltoon",
    "boysarequirky",
    "PewdiepieSubmissions",
    "AdventurersLeague",
    "CrusaderKings",
    "magicTCG",
    "survivor",
    "The10thDentist",
    "copypasta",
    "goodanimemes",
    "GachaLifeCringe",
    "phish",
    "WatchesCirclejerk",
    "HFY",
    "leopardsatemyface",
    "politicalhumor",
    "SocialDemocracy",
    "JoeRogan",
    "thedavidpakmanshow",
    "ShowerThoughts",
    "DoesAnybodyElse",
    "changemyview",
    "crazyideas",
    "howtonotgiveafuck",
    "tipofmytongue",
    "quotes",
    "casualconversation",
    "makenewfriendshere",
    "relationship_advice",
    "raisedbynarcissists",
    "legaladvice",
    "advice",
    "amitheasshole",
    "mechanicadvice",
    "toastme",
    "IAmA",
    "ExplainlikeIAmA",
    "AMA",
    "casualiama",
    "de_Iama",
    "whowouldwin",
    "wouldyourather",
    "scenesfromahat",
    "AskOuija",
    "themonkeyspaw",
    "shittysuperpowers",
    "godtiersuperpowers",
    "decreasinglyverbose",
    "jesuschristouija",
    "whatisthisthing",
    "answers",
    "NoStupidQuestions",
    "amiugly",
    "whatsthisbug",
    "samplesize",
    "tooafraidtoask",
    "whatsthisplant",
    "isitbullshit",
    "morbidquestions",
    "AskReddit",
    "ShittyAskScience",
    "TrueAskReddit",
    "AskScienceFiction",
    "AskOuija",
    "AskScience",
    "askhistorians",
    "askculinary",
    "AskSocialScience",
    "askengineers",
    "askphilosophy",
    "askdocs",
    "askwomen",
    "askmen",
    "askgaybros",
    "askredditafterdark",
    "asktransgender",
    "askmenover30",
    "tifu",
    "self",
    "confession",
    "fatpeoplestories",
    "confessions",
    "storiesaboutkevin",
    "talesfromtechsupport",
    "talesfromretail",
    "techsupportmacgyver",
    "idontworkherelady",
    "TalesFromYourServer",
    "KitchenConfidential",
    "TalesFromThePizzaGuy",
    "TalesFromTheFrontDesk",
    "talesfromthecustomer",
    "talesfromcallcenters",
    "talesfromthesquadcar",
    "talesfromthepharmacy",
    "starbucks",
    "pettyrevenge",
    "prorevenge",
    "nuclearrevenge",
    "nosleep",
    "LetsNotMeet",
    "Glitch_in_the_Matrix",
    "shortscarystories",
    "thetruthishere",
    "UnresolvedMysteries",
    "UnsolvedMysteries",
    "depression",
    "SuicideWatch",
    "Anxiety",
    "foreveralone",
    "offmychest",
    "socialanxiety",
    "trueoffmychest",
    "unsentletters",
    "rant",
    "gaming",
    "Games",
    "outside",
    "truegaming",
    "gamernews",
    "gamephysics",
    "webgames",
    "IndieGaming",
    "patientgamers",
    "AndroidGaming",
    "randomactsofgaming",
    "speedrun",
    "gamemusic",
    "emulation",
    "MMORPG",
    "gamecollecting",
    "hitboxporn",
    "gamingcirclejerk",
    "gamingdetails",
    "gaming4gamers",
    "retrogaming",
    "itemshop",
    "GameDeals",
    "steamdeals",
    "PS4Deals",
    "freegamesonsteam",
    "shouldibuythisgame",
    "nintendoswitchdeals",
    "freegamefindings",
    "xboxone",
    "oculus",
    "vive",
    "paradoxplaza",
    "pcmasterrace",
    "pcgaming",
    "gamingpc",
    "steam",
    "linux_gaming",
    "nintendo",
    "3DS",
    "wiiu",
    "nintendoswitch",
    "3dshacks",
    "amiibo",
    "sony",
    "PS3",
    "playstation",
    "vita",
    "PSVR",
    "playstationplus",
    "ps5",
    "PS4",
    "PS4Deals",
    "DotA2",
    "starcraft",
    "smashbros",
    "dayz",
    "civ",
    "KerbalSpaceProgram",
    "masseffect",
    "clashofclans",
    "starbound",
    "heroesofthestorm",
    "terraria",
    "dragonage",
    "citiesskylines",
    "smite",
    "bindingofisaac",
    "eve",
    "starcitizen",
    "metalgearsolid",
    "elitedangerous",
    "bloodborne",
    "monsterhunter",
    "warframe",
    "undertale",
    "thedivision",
    "stardewvalley",
    "nomansskythegame",
    "totalwar",
    "pathofexile",
    "ClashRoyale",
    "crusaderkings",
    "dwarffortress",
    "eu4",
    "thesims",
    "assassinscreed",
    "playrust",
    "forhonor",
    "stellaris",
    "kingdomhearts",
    "blackdesertonline",
    "factorio",
    "Warhammer",
    "splatoon",
    "rimworld",
    "Xcom",
    "streetfighter",
    "paydaytheheist",
    "MonsterHunterWorld",
    "Seaofthieves",
    "cyberpunkgame",
    "warhammer40k",
    "paladins",
    "osugame",
    "spidermanps4",
    "persona5",
    "mountandblade",
    "deadbydaylight",
    "farcry",
    "hoi4",
    "warthunder",
    "grandorder",
    "divinityoriginalsin",
    "escapefromtarkov",
    "theexpanse",
    "darkestdungeon",
    "forza",
    "godofwar",
    "ark",
    "bioshock",
    "edh",
    "summonerswar",
    "duellinks",
    "arma",
    "pathfinderrpg",
    "footballmanagergames",
    "kingdomcome",
    "subnautica",
    "thelastofus",
    "doom",
    "jrpg",
    "apexlegends",
    "smashbrosultimate",
    "brawlstars",
    "anthemthegame",
    "mortalkombat",
    "sekiro",
    "TeamfightTactics",
    "afkarena",
    "valorant",
    "amongus",
    "genshin_impact",
    "stardustcrusaders",
    "animalcrossing",
    "acturnips",
    "borderlands",
    "borderlands2",
    "borderlands3",
    "DarkSouls",
    "DarkSouls2",
    "DarkSouls3",
    "diablo",
    "diablo3",
    "elderscrollsonline",
    "ElderScrolls",
    "teslore",
    "Skyrim",
    "skyrimmods",
    "fallout",
    "fo4",
    "fo76",
    "fireemblem",
    "FireEmblemHeroes",
    "FortniteBR",
    "Fortnite",
    "FortniteBattleRoyale",
    "Fortnitecompetitive",
    "FortniteLeaks",
    "GrandTheftAutoV",
    "gtav",
    "gtaonline",
    "hearthstone",
    "CompetitiveHS",
    "customhearthstone",
    "minecraft",
    "feedthebeast",
    "minecraftbuilds",
    "minecraftsuggestions",
    "overwatch",
    "competitiveoverwatch",
    "overwatchuniversity",
    "Overwatch_Memes",
    "Overwatch_Porn",
    "PUBATTLEGROUNDS",
    "PUBG",
    "pubgxboxone",
    "pubgmobile",
    "reddeadredemption",
    "reddeadredemption2",
    "rocketleague",
    "rocketleagueexchange",
    "witcher",
    "gwent",
    "tf2",
    "starwarsbattlefront",
    "rainbow6",
    "titanfall",
    "shittyrainbow6",
    "battlefield_4",
    "battlefield",
    "battlefield_one",
    "battlefieldv",
    "blackops3",
    "CODZombies",
    "callofduty",
    "WWII",
    "blackops4",
    "codcompetitive",
    "modernwarfare",
    "codwarzone",
    "GlobalOffensive",
    "csgo",
    "halo",
    "haloonline",
    "fifa",
    "nba2k",
    "DestinyTheGame",
    "fireteams",
    "destiny2",
    "raidsecrets",
    "leagueoflegends",
    "summonerschool",
    "LoLeventVODs",
    "wow",
    "guildwars2",
    "swtor",
    "classicwow",
    "ffxiv",
    "FinalFantasy",
    "ffxv",
    "Pokemon",
    "friendsafari",
    "pokemontrades",
    "PokemonSwordAndShield",
    "pokemonmasters",
    "shinypokemon",
    "pokemonromhacks",
    "pokemongo",
    "TheSilphRoad",
    "pokemongospoofing",
    "pokemongofriends",
    "pokemonletsgo",
    "Runescape",
    "2007scape",
    "zelda",
    "breath_of_the_wild",
    "aceattorney",
    "wallstreetbets",
    "stocks",
    "oppai_suika_testing",
    "programming",
]

print("starting...")


def get_comment_chain(comment):
    if not isinstance(comment, praw.models.Comment):
        return
    parent_comment = get_comment_chain(comment.parent())
    if parent_comment is not None:
        return [comment, *parent_comment]
    else:
        return [comment]


def get_submission(comment):
    if not isinstance(comment, praw.models.Comment):
        return comment
    else:
        return get_submission(comment.parent())


def init_stream(subreddit_name: str):
    subreddit = reddit.subreddit(subreddit_name)
    return subreddit.stream.comments(pause_after=-1)


User = Query()
comment_streams = [init_stream(subreddit) for subreddit in subreddits]
while True:
    for comment_stream in comment_streams:
        for comment in comment_stream:
            if comment is None:
                break
            if re.search("!objection-*bot", comment.body, re.IGNORECASE):
                if len(db.search(User.id == comment.id)) == 0:
                    try:
                        print(
                            f"doing {comment.id} (https://www.reddit.com{comment.permalink})"
                        )

                        # handle metadata
                        print(f"handling metadata...")
                        db.insert({"id": comment.id})
                        comments = list(reversed(get_comment_chain(comment)))[:-1]
                        authors = [comment.author.name for comment in comments]
                        most_common = [t[0] for t in Counter(authors).most_common()]
                        submission = get_submission(comment)

                        # generate video
                        output_filename = f"{comment.id}.mp4"
                        print(f"generating video {output_filename}...")
                        characters = anim.get_characters(most_common)
                        anim.comments_to_scene(
                            comments, characters, output_filename=output_filename
                        )

                        # upload video
                        print(f"uploading video...")
                        response = _spaw.videoUpload(output_filename)
                        print(response)
                        comment.reply(
                            f"[Here's the video!](https://streamable.com/{response['shortcode']})"
                        )

                        print(f"done {comment.id}")
                    except Exception as e:
                        print(e)
