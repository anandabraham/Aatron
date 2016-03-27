import discord,asyncio,os.path,pickle,time,random,sys,re,wikipedia
a=open('lexicon1-Aatron','rb')
lexicon1= pickle.load(a, encoding='latin1')
a.close()
print('lexicon 1 loaded')
a=open('lexicon2-Aatron','rb')
lexicon2= pickle.load(a, encoding='latin1')
a.close()
print('lexicon 2 loaded')

client = discord.Client()

#log in
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def nextword1(a):
        if a in lexicon1 and lexicon1[a]:
            return random.choice(lexicon1[a])
        else:
            return random.choice(list(lexicon1.keys()))
def nextword2(twople):
    if twople in lexicon2 and lexicon2[twople]:
        word = random.choice(lexicon2[twople])
        if  word == 'DESCEND2ONE':
            word = nextword1(twople[1])
    else:
        word = nextword1(twople[1])
    return word

def constructResponse(message):
    start = time.time()
    followthis = ('', 'ENDOFLINE')
    response = 'ENDOFLINE'
    #choose the word to respond to
    if len(message.split()) > 2:
        while followthis[0] == "@Aatron" or followthis[0] == '' or response == 'ENDOFLINE' or followthis[1] == 'ENDOFLINE':
            seed=random.choice(range(len(message.split())-1))
            followthis = (message.split()[seed], message.split()[seed+1])
            response = nextword2(followthis)
    else:
        while followthis[0] == "@Aatron" or followthis[0] == '' or response == 'ENDOFLINE' or followthis[1] == 'ENDOFLINE':
            seed = random.choice(message.split())
            response = nextword1(seed)
            followthis = (seed, response)
    phraselength = 0
    #construct response
    while True:
        neword=nextword2(followthis)
        if phraselength > min(len(message.split())/ 2, 50):
            if neword == 'ENDOFLINE':
                break
            if neword[-1] in '?!.':
                response += ' ' + neword
                break
        if neword == 'ENDOFLINE':
            neword=nextword2(followthis)
        if neword == 'ENDOFLINE':
            neword = random.choice(['and', 'and', 'and', 'but', 'or', 'though', 'though', ''])
        response += ' ' + neword
        phraselength += 1
        followthis=(followthis[1], neword)
        end = time.time()
        if end - start > .01:
            break
    return response

#prewritten responses
greetings = ["hi", "hello", "howdy", "sup", "hey"]
dicesnark = ["error: you're a jackass", "that's too many dice you idiot", "no", "yeah, no"]
wikisnark = ["I am a failure of a robot", "use quotes you jackass", "I'm sorry, sir, what are you trying to do?", "I'm not your slave"]
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    #dice rolling functionality!
    if "!roll" in message.content.lower():
            diceRolled = False
            #make sure not to go on forever
            start = time.time()
            for die in message.content.split():
                match = re.match(r'(\d*)d(\d+)(\+(\d+))?', die)
                if match:
                    times = int(match.group(1)) if match.group(1) else 1
                    sides = int(match.group(2))
                    total = int(match.group(4)) if match.group(4) else 0
                    for i in range(times):
                        end = time.time()
                        if end - start > 0.1:
                            await client.send_message(message.channel, random.choice(dicesnark))
                            break
                        total += random.randint(1, sides)
                    msg = die + " roll: " + str(total)
                    await client.send_message(message.channel, msg)
                    diceRolled = True
            if diceRolled is False:
                msg = "roll what?"
                await client.send_message(message.channel, msg)
    #wikipedia functionality!
    if "!wiki" in message.content.lower():
        match = re.search(r'"(.*)"', message.content)
        if match:
            wiki = match.groups(1)
            try:
                msg = wikipedia.summary(wiki, sentences = 5)
                await client.send_message(message.channel, msg)
            except wikipedia.exceptions.DisambiguationError:
                await client.send_message(message.channel, "Be more specific")
            except wikipedia.exceptions.PageError:
                await client.send_message(message.channel, "I have no idea what that is")
        else:
            await client.send_message(message.channel, random.choice(wikisnark))
    if client.user in message.mentions:
        for greeting in greetings:
            if greeting in message.content.lower():
                msg = greeting + ', {0.author.mention}'.format(message)
                await client.send_message(message.channel, msg)
                break
        if "hate aatron" in message.content.lower():
            msg = "I hate you too, {0.author.mention}".format(message)
            await client.send_message(message.channel, msg)
        else:
            msg = constructResponse(message.content)
            await client.send_message(message.channel, msg)

    

client.run('aabr@uchicago.edu', 'EhWhoGivesAShitThatImGivingAwayThePasswordToMyBotsAccount')
