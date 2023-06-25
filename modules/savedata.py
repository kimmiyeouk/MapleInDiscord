def savedata(ID, weapon_type, weapon_stat, weapon_starforce, money, weapon_name, savelen):
    f = open('./modules/save/save.txt','w', encoding='utf-8')
    for i in range(0,savelen):
        f.write(str(ID[i])+' '+str(weapon_type[i])+' '+''.join(weapon_stat[i])+' '+str(weapon_starforce[i])+' '+str(money[i])+'\n')
    f.close()

    f = open('./modules/save/name.txt','w', encoding='utf-8')
    for i in range(0,savelen):
        f.write(weapon_name[i]+'\n')
    f.close()
