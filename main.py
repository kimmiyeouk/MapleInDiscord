import discord
import random as r
import time as t

from modules import System_data as s
from modules import savedata


f = open('./modules/save/save.txt', 'r', encoding='utf-8')
buff = f.readlines()

nowtime = 0

ID = []
weapon_name = []
weapon_type = []
weapon_stat = []
weapon_starforce = []
money = []

for i in range(0, len(buff)):
    buff[i] = buff[i].rstrip('\n')
    ID.append(buff[i].split(' ')[0])
    weapon_type.append(buff[i].split(' ')[1])
    weapon_stat.append(list(buff[i].split(' ')[2]))
    weapon_starforce.append(int(buff[i].split(' ')[3]))
    money.append(int(buff[i].split(' ')[4]))

f.close()
f = open('./modules/save/win.txt', 'r', encoding='utf-8')
win_message = f.readlines()
for i in range(0, len(win_message)):
    win_message[i] = win_message[i].rstrip('\n')

f.close()

f = open('./modules/save/win_image.txt','r',encoding='utf-8')
win_image = f.readlines()
for i in range(0, len(win_image)):
    win_image[i] = win_image[i].rstrip('\n')

f.close()

f = open('./modules/save/commands', 'r', encoding='utf-8')
commands = f.readlines()
f.close()

f = open('./modules/save/name.txt', 'r', encoding='utf-8')
buff = f.readlines()
for i in range(0, len(buff)):
    buff[i] = buff[i].rstrip('\n')
    weapon_name.append(buff[i])

f.close()

print(ID[0])

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

f = open('./modules/save/config','r',encoding='utf-8')
token = f.readline().rstrip('\n')
f.close()
print("다음으로 로그인 :",token)
# 1-6에서 생성된 토큰을 이곳에 입력해주세요.


# 봇이 구동되었을 때 동작되는 코드입니다.

A = ''
B = ''
AA = -1
BB = -1
betting = 0

@client.event
async def on_ready():
    print("Logged in as ") #화면에 봇의 아이디, 닉네임이 출력됩니다.
    print(client.user.name)
    print(client.user.id)
    print("===========")
    # 디스코드에는 현재 본인이 어떤 게임을 플레이하는지 보여주는 기능이 있습니다.
    # 이 기능을 사용하여 봇의 상태를 간단하게 출력해줄 수 있습니다.
    game = discord.Game("2학년 4반 1번 김동현에게 개발당")
    await client.change_presence(status=discord.Status.online, activity=game)

# 봇이 새로운 메시지를 수신했을때 동작되는 코드입니다.
@client.event
async def on_message(message):
    global ID
    global weapon_type
    global weapon_stat
    global weapon_starforce
    global weapon_name
    global money
    global A
    global B
    global AA
    global BB
    global betting
    global nowtime


    if message.author.bot: #만약 메시지를 보낸사람이 봇일 경우에는
        return None #동작하지 않고 무시합니다.

    id = message.author.id #id라는 변수에는 메시지를 보낸사람의 ID를 담습니다.
    channel = message.channel #channel이라는 변수에는 메시지를 받은 채널의 ID를 담습니다.

    if message.content:
        if t.time() - nowtime > 60 and A != '':
            print(1)
            A = ''
            B = ''
            AA = 0
            BB = 0
            betting = 0
    if message.content:
        f = 0
        ran = 0
        monran = r.randint(10000,20000)
        maxran = 20
        for i in range(0,len(ID)):
            if ID[i] == str(id):
                f = 1
                break
        if f == 1:
            maxran -= int(weapon_stat[i][0]) * 2
            ran = r.randint(1,maxran)
            if ran == 1:
                monran = int(monran * (1 + int(weapon_stat[i][1]) * 0.1))
                money[i] += monran
                savedata.savedata(ID,weapon_type,weapon_stat,weapon_starforce,money,weapon_name,len(ID))
    if message.content =='!무기파괴':
        f = 0
        for i in range(0,len(ID)):
            if ID[i] == str(id):
                f = 1
                break
        if f == 1:
            weapon_starforce[i] = 0
            weapon_name[i] = '0'
            weapon_type[i] = -1
            weapon_stat[i] = list('0000000')
            savedata.savedata(ID, weapon_type, weapon_stat, weapon_starforce, money, weapon_name, len(ID))
            await channel.send('```무기가 파괴되었습니다.```')
            return None
        await channel.send('```세이브가 존재하지 않습니다.\n!등록 명령어를 통해 세이브를 등록해주세요.```')
    if message.content == '!강화':
        f = 0
        rnd = r.randint(1,99)
        for i in range(0,len(ID)):
            if ID[i] == str(id):
                f = 1
                if money[i] < 30000:
                    await channel.send('```잔액이 부족합니다.```')
                    return None
                if weapon_name[i] == '0':
                    await channel.send('```무기가 존재하지 않습니다.```')
                    return None
                break
        if f == 1 and weapon_starforce[i] != 11:
            money[i] -= 30000
            if rnd in range(1,s.starforce_success[weapon_starforce[i]]):
                weapon_starforce[i] += 1
                if weapon_starforce[i] == 11:
                    await channel.send('<@{}>```마스터리 강화에 성공하였습니다!\n10성 -> 마스터리 레벨```'.format(str(id)))
                else:
                    await channel.send('<@{}>```강화에 성공하였습니다!\n{}성 -> {}성```'.format(str(id),str(weapon_starforce[i]-1),str(weapon_starforce[i])))
            elif rnd in range(s.starforce_success[weapon_starforce[i]],s.starforce_success[weapon_starforce[i]] + s.starforce_fail[weapon_starforce[i]]):
                await channel.send('<@{}>```강화에 실패하였습니다...```'.format(str(id)))
            elif rnd in range(s.starforce_success[weapon_starforce[i]] + s.starforce_fail[weapon_starforce[i]], s.starforce_success[weapon_starforce[i]] + s.starforce_fail[weapon_starforce[i]] + s.starforce_downgrade[weapon_starforce[i]]):
                weapon_starforce[i] -= 1
                await channel.send('<@{}>```강화에 실패하였습니다...\n{}성 -> {}성```'.format(str(id), str(weapon_starforce[i]+1),str(weapon_starforce[i])))
            elif rnd in range(s.starforce_success[weapon_starforce[i]] + s.starforce_fail[weapon_starforce[i]] + s.starforce_downgrade[weapon_starforce[i]], s.starforce_success[weapon_starforce[i]] + s.starforce_fail[weapon_starforce[i]] + s.starforce_downgrade[weapon_starforce[i]]+s.starforce_destroy[weapon_starforce[i]]):
                weapon_starforce[i] = 0
                weapon_name[i] = '0'
                weapon_type[i] = -1
                weapon_stat[i] = list('0000000')
                await channel.send('<@{}>```강화에 실패하였습니다...\n무기가 파괴되었습니다.```'.format(str(id)))
            else:
                print('error')
                print(rnd)
                money[i] += 30000
                await channel.send('```알 수 없는 오류가 발생하였습니다.```')
            savedata.savedata(ID,weapon_type,weapon_stat,weapon_starforce,money,weapon_name,len(ID))
            return None
        await channel.send('```세이브가 존재하지 않습니다.\n!등록 명령어를 통해 세이브를 등록해주세요.```')
        return None
    if message.content == '!명령어':
        msg = '```'
        for i in range(0,len(commands)):
            msg += commands[i]
        msg +='```'
        await channel.send(msg)
        return None

    if message.content == '!등록':
        f = 0
        for i in range(0,len(ID)):
            if ID[i] == str(id):
                f = 1
                break
        if f == 0:
            ID.append(str(id))
            weapon_type.append(-1)
            weapon_stat.append(list('0000000'))
            weapon_starforce.append(0)
            weapon_name.append('0')
            money.append(100000)
            savedata.savedata(ID,weapon_type,weapon_stat,weapon_starforce,money,weapon_name,len(ID))
            await channel.send('```등록되었습니다! 이제부터 봇 이용이 가능합니다!```')
        else:
            await channel.send('```이미 등록되었습니다.```')
        return None
    if message.content == '!마법':
        await channel.send('```!마법 <마법>\n확인 가능한 마법 : 가속, 채굴, 강타, 날카로움, 휘두르기, 관통, 신성```')
        return None
    if message.content.startswith('!마법'):
        inp = message.content
        inp = inp.split()[1]
        if inp == '가속':
            await channel.send('```채팅 시 돈이 채굴되는 확률이 증가합니다.\n1클래스당 5%의 확률이 증가합니다.```')
        elif inp == '채굴':
            await channel.send('```채팅 시 채굴되는 돈의 양이 증가합니다.\n1클래스당 돈의 양이 10%만큼 증가합니다.```')
        elif inp == '강타':
            await channel.send('```전투력이 증가합니다.\n1클래스당 전투력이 2만큼 증가합니다.```')
        elif inp == '날카로움':
            await channel.send('```도끼를 상대로 한 전투력이 증가합니다.\n1클래스당 전투력이 3만큼 증가합니다.```')
        elif inp == '휘두르기':
            await channel.send('```창을 상대로 한 전투력이 증가합니다.\n1클래스당 전투력이 3만큼 증가합니다.```')
        elif inp == '관통':
            await channel.send('```지팡이를 상대로 한 전투력이 증가합니다.\n1클래스당 전투력이 3만큼 증가합니다.```')
        elif inp == '신성':
            await channel.send('```검을 상대로 한 전투력이 증가합니다.\n1클래스당 전투력이 3만큼 증가합니다.```')
        else:
            await channel.send('```!마법 <마법>\n확인 가능한 마법 : 가속, 채굴, 강타, 날카로움, 휘두르기, 관통, 신성```')
    if message.content == '!무기':
        f = 0
        S = ''
        SS = ''
        SSS = ''
        pow = ''
        for i in range(0,len(ID)):
            if ID[i] == str(id):
                f = 1
                if weapon_name[i] == '0':
                    await channel.send('```무기가 존재하지 않습니다.\n!무기생성 명령어를 입력해주세요.```')
                    return None
                break
        if f == 1:
            for j in range(0, s.enchant_sum):
                if weapon_stat[i][j] != '0':
                    SS += '\n-'+s.enchant_name[j]+' '+weapon_stat[i][j]+'클래스'
            if weapon_starforce[i] == 0:
                SSS = '비활성화\n-성공확률 : 100%\n-실패확률 : 0%\n-하락확률 : 0%\n-파괴확률 : 0%' 
            elif weapon_starforce[i] == 11:
                SSS = '마스터리 레벨\n강화 불가능'
            else:
                SSS = str(weapon_starforce[i])+'성\n-성공확률 : {}%\n-실패확률 : {}%\n-하락확률 : {}%\n-파괴확률 : {}%'.format(s.starforce_success[weapon_starforce[i]],s.starforce_fail[weapon_starforce[i]],s.starforce_downgrade[weapon_starforce[i]],s.starforce_destroy[weapon_starforce[i]])
            S = '```무기\n\n이름 : '+weapon_name[i]+'\n\n무기 타입 : '+s.weapon_type[int(weapon_type[i])]+'\n\n마법 : '+SS+'\n\n강화 : '+SSS
            pow = '\n\n최소 전투력 : ' + str((1 + s.starforce_power[weapon_starforce[i]] + (int(weapon_stat[i][2]) * 2))) + '```'
            await channel.send('<@{}>'.format(id)+S+pow)
            return None
        await channel.send('```세이브가 존재하지 않습니다.\n!등록 명령어를 통해 세이브를 등록해주세요.```')
        return None
    if message.content == '!내돈':
        f = 0
        for i in range(0,len(ID)):
            if ID[i] == str(id):
                f = 1
                break;
        if f == 1:
            await channel.send('<@{}>```잔액 : '.format(id)+str(money[i])+'원```')
            return None
        await channel.send('```세이브가 존재하지 않습니다.\n!등록 명령어를 통해 세이브를 등록해주세요.```')
        return None
    if message.content == '!무기생성':
        await channel.send('```!무기생성 <검|도끼|창|지팡이> [이름]\n무기를 생성하면 5만원이 소모되며, 무작위로 마법 하나가 부여됩니다.```')
        return None
    if message.content == '!마법부여':
        f = 0
        ran = 0
        lev = 0
        for i in range(0,len(ID)):
            if ID[i] == str(id):
                f = 1
                if weapon_name[i] != '0':
                    f = 2
                    if money[i] < 25000:
                        await channel.send('```잔액이 부족합니다!```')
                        return None
                break
        if f == 2:
            weapon_stat[i] = list('0000000')
            money[i] -= 25000
            if weapon_starforce[i] == 11:
                for j in range(0,4):
                    ran = r.randint(0,s.enchant_sum-1)
                    lev = r.randint(1,5)
                    weapon_stat[i][ran] = str(lev)
            else:
                for j in range(0,3):
                    ran = r.randint(0, s.enchant_sum - 1)
                    lev = r.randint(1, 5)
                    weapon_stat[i][ran] = str(lev)
            savedata.savedata(ID,weapon_type,weapon_stat,weapon_starforce,money,weapon_name,len(ID))
            await channel.send('<@{}>```마법이 부여되었습니다!\n!무기 명령어를 통해 자신의 무기를 확인하세요!```'.format(str(id)))
            return None
        elif f == 1:
            await channel.send('```무기가 존재하지 않습니다.\n!무기생성 명령어를 입력해주세요.```')
            return None
        await channel.send('```세이브가 존재하지 않습니다.\n!등록 명령어를 통해 세이브를 등록해주세요.```')
        return None


    if message.content.startswith('!무기생성'):
        inp = message.content
        ty = inp.split(' ')[1]
        if ty == '검':
            sl = inp.find(ty) + 2
        if ty == '도끼':
            sl = inp.find(ty) + 3
        if ty == '창':
            sl = inp.find(ty) + 2
        if ty == '지팡이':
            sl = inp.find(ty) + 4
        temp = inp.split()
        name = inp[sl:len(inp)]
        f = 0
        g = 0
        if len(temp) == 2:
            await channel.send('```!무기생성 <검|도끼|창|지팡이> [이름]\n무기를 생성하면 5만원이 소모되며, 무작위로 마법 하나가 부여됩니다.```')
            return None
        for i in range(0,len(ID)):
            if ID[i] == str(id):
                f = 1
                if weapon_name[i] != '0':
                    g = 1
                if money[i] < 50000:
                    await channel.send('```잔액이 부족합니다.```')
                    return None
                break
        if f == 1 and g == 0:
            money[i] -= 50000
            if ty == '검':
                weapon_type[i] = 0
                weapon_stat[i][r.randint(0, s.enchant_sum - 1)] = str(r.randint(1,5))
                weapon_name[i] = name
            elif ty == '도끼':
                weapon_type[i] = 1
                weapon_stat[i][r.randint(0, s.enchant_sum - 1)] = str(r.randint(1,5))
                weapon_name[i] = name
            elif ty == '창':
                weapon_type[i] = 2
                weapon_stat[i][r.randint(0, s.enchant_sum - 1)] = str(r.randint(1,5))
                weapon_name[i] = name
            elif ty == '지팡이':
                weapon_type[i] = 3
                weapon_stat[i][r.randint(0, s.enchant_sum - 1)] = str(r.randint(1,5))
                weapon_name[i] = name
            else:
                await channel.send('```존재하지 않는 무기 속성입니다.```')
                return None
            savedata.savedata(ID,weapon_type,weapon_stat,weapon_starforce,money,weapon_name,len(ID))
            await channel.send('```무기 생성이 완료되었습니다!\n!무기 명령어를 통해 자신의 무기를 확인하세요!```')
            return None
        if f == 1 and g == 1:
            await channel.send('```이미 무기가 존재합니다.\n기존 무기를 삭제하려면 !삭제 명령어를 입력해주세요.```')
            return None
        await channel.send('```세이브가 존재하지 않습니다.\n!등록 명령어를 통해 세이브를 등록해주세요.```')
        return None
    if message.content == '!배틀':
        await channel.send('```!배틀 [멘션] [배팅금]```')
        return None

    if message.content.startswith('!배틀'):
        print(1)
        if A != '':
            await channel.send('```이미 배틀중입니다!\n다른 유저의 배틀이 끝날때까지 기다려주세요!```')
            return None
        f = 0
        g = 0
        inp = message.content
        n = inp.split(' ')[1]
        n = n[2:20]
        print(n)
        bet = int(inp.split(' ')[2])
        #if str(id) == n:
            #await channel.send('```나 자신과 배틀 할 수 없습니다.```')
            #return None
        if bet < 0:
            await channel.send('```음수값은 배팅할 수 없습니다.```')
            return None
        for i in range(0,len(ID)):
            if ID[i] == str(id):
                f = 1
                if money[i] < bet:
                    await channel.send('```배팅을 위한 잔액이 부족합니다...```')
                    return None
                break
        for j in range(0,len(ID)):
            if ID[j] == n:
                g = 1
                if money[j] < bet:
                    await channel.send('```배팅을 위한 상대의 잔액이 부족합니다...```')
                    return None
                break
        print(f,g)
        if f == 1 and g == 1:
            nowtime = t.time()
            A = str(id)
            B = n
            AA = i
            BB = j
            betting = bet
            await channel.send('<@{}>님이 <@{}>님에게 배틀을 신청하셨습니다!```배팅금 : {}원\n\n수락하시려면 !수락 명령어를,\n거절하시려면 !거절 명령어를 입력해주세요.\n\n60초 동안 아무런 반응이 없으면 배틀은 자동 취소됩니다.```'.format(A,B,str(bet)))
        return None
    if message.content == '!거절':
        if str(id) != B:
            return None
        await channel.send('<@{}>```배틀이 거절되었습니다.```'.format(A))
        A = ''
        B = ''
        AA = 0
        BB = 0
        betting = 0
        return None
    if message.content == '!수락':
        if str(id) != B:
            await channel.send('```배틀 신청을 받지 않았습니다.```')
            return None
        AP = 1 + s.starforce_power[weapon_starforce[AA]] + (2 * int(weapon_stat[AA][2]))
        BP = 1 + s.starforce_power[weapon_starforce[BB]] + (2 * int(weapon_stat[BB][2]))
        msg = ''
        if int(weapon_type[BB]) == 0:
            AP += int(weapon_stat[AA][6]) * 3
        if int(weapon_type[BB]) == 1:
            AP += int(weapon_stat[AA][3]) * 3
        if int(weapon_type[BB]) == 2:
            AP += int(weapon_stat[AA][4]) * 3
        if int(weapon_type[BB]) == 3:
            AP += int(weapon_stat[AA][5]) * 3
        if int(weapon_type[AA]) == 0:
            BP += int(weapon_stat[BB][6]) * 3
        if int(weapon_type[AA]) == 1:
            BP += int(weapon_stat[BB][3]) * 3
        if int(weapon_type[AA]) == 2:
            BP += int(weapon_stat[BB][4]) * 3
        if int(weapon_type[AA]) == 3:
            BP += int(weapon_stat[BB][5]) * 3
        rnd = r.randint(1,AP + BP-1)
        im = r.randint(0, len(win_message) - 1)
        if rnd in range(1,AP):
            money[AA] += betting
            money[BB] -= betting
            #msg = '<@{}>님이 <@{}>'.format(A,B)+win_message[r.randint(0,len(win_message)-1)]
            embed = discord.Embed(title="배틀 결과")
            embed.add_field(name='승리', value='<@{}>'.format(A), inline=True)
            embed.add_field(name='패배', value='<@{}>'.format(B), inline=True)
            embed.add_field(name='상금', value='{}원'.format(betting), inline=True)
            embed.add_field(name='승리 사유', value='<@{}>님이 <@{}>'.format(A,B)+win_message[im])
            embed.set_image(url=win_image[im])
            print(win_image[im])
            await channel.send(embed=embed)
        elif rnd in range(AP,AP+BP):
            money[AA] -= betting
            money[BB] += betting
            #msg = '<@{}>님이 <@{}>'.format(B, A) + win_message[r.randint(0, len(win_message)-1)]
            embed = discord.Embed(title="배틀 결과")
            embed.add_field(name='승리', value='<@{}>'.format(B), inline=True)
            embed.add_field(name='패배', value='<@{}>'.format(A), inline=True)
            embed.add_field(name='상금', value='{}원'.format(betting), inline=True)
            embed.add_field(name='승리 사유',value='<@{}>님이 <@{}>'.format(B, A) + win_message[im])
            embed.set_image(url=win_image[im])
            print(win_image[im])
            await channel.send(embed=embed)
        A = ''
        B = ''
        AA = 0
        BB = 0
        betting = 0
        return None
client.run(token)
