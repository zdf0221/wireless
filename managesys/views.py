# coding=utf-8
import json

import datetime

import math
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from .forms import *

from managesys.models import *


# Create your views here.

def index(request):
    # 首页
    return render_to_response("index.html")


def register(request):
    #  如果是POST发送表单
    if request.method == 'POST':
        # 实例化表单
        form = registerForm(request.POST)
        # 检验表单合理性，然后读取数据
        if form.is_valid():
            ID = form.cleaned_data['personalID']
            username = form.cleaned_data['username']
            # 新建用户
            user.objects.get_or_create(personalID=ID, username=username)
            request.session['personalID'] = ID
            request.session['username'] = username
            return render_to_response("registerSuccess.html")
    else:
        # 正常创建表单
        form = registerForm()
        return render(request, 'registerForm.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)

        if form.is_valid():
            ID = form.cleaned_data['personalID']
            name = form.cleaned_data['username']
            # 根据身份证号和姓名筛选客户
            person = user.objects.filter(personalID=ID).filter(username=name)
            if not person:
                # 如果数据库中没有此人
                return render_to_response("loginFailed.html")
            else:
                # 保存会话信息
                request.session['personalID'] = person[0].personalID
                request.session['username'] = person[0].username
                # 会话标签
                print person[0].personalID
                personList = []
                for i in range(len(person)):
                    personList.append(person[i].personalID)
                    personList.append(person[i].username)
                    personList.append(person[i].accountNumber)
                return render(request, "loginSuccess.html", {'personList': personList})

    else:
        form = loginForm()
        return render(request, 'loginForm.html', {'form': form})


def createAccount(request):
    curUser = request.session['username']
    packList = []  # 套餐列表
    numList = []  # 号码列表

    # 打印所有套餐信息
    pack = package.objects.all()
    for i in range(len(pack)):
        tempPack = ""
        tempPack += pack[i].packNumber + ":"
        tempPack += pack[i].packName + " "
        tempPack += pack[i].packType + " "
        tempPack += pack[i].packFee + " "
        packList.append(tempPack)

    # 打印所有可用号码信息
    num = number.objects.all()
    for i in range(len(num)):
        tempNum = ""
        tempNum += num[i].phoneNumber + " "
        numList.append(tempNum)

    if request.method == 'POST':
        form = createAccountForm(request.POST)
        if form.is_valid():
            packNumber = form.cleaned_data['packNumber']
            chargeFee = form.cleaned_data['chargeFee']
            phoneNumber = form.cleaned_data['phoneNumber']
            userID = user.objects.filter(personalID=request.session['personalID'])
            # 新建user信息（开户）
            account.objects.create(
                accountNumber=phoneNumber,
                packNumber=packNumber,
                accountFee=package.objects.get(packNumber=packNumber).packFee,
                #  username=request.session['username'],
                personalID=userID[0],
                balance=chargeFee - int(package.objects.get(packNumber=packNumber).packFee),
                status="available"
            )
            # 从号码库删除开户用的号码
            number.objects.filter(phoneNumber=phoneNumber).delete()
            return render(request, 'createAccountSuccess.html', {'curUser': curUser,
                                                                 'packList': packList,
                                                                 'numList': numList,
                                                                 'form': form})
    else:
        form = createAccountForm()
        return render(request, 'createAccount.html', {'curUser': curUser,
                                                      'packList': packList,
                                                      'numList': numList,
                                                      'form': form})


def userinfo(request):
    if request.is_ajax():
        #  ajax这部分还有问题，暂且不用
        return render_to_response('userinfo.html')
        '''
        print "收到刷新请求，开始刷新用户数据"
        #  筛选user内的account
        userID = request.session['personalID']
        accountSet = account.objects.filter(personalID__personalID__exact=userID)
        #  对每一个accountNumber，依次处理traffic，sms，data
        for i in range(len(accountSet)):
            print accountSet[i].accountNumber
            trafficSet = traffic.objects.filter(callerNumber=accountSet[i].accountNumber)
            for j in range(len(trafficSet)):
                print trafficSet[j].id
            if queryset[i].callType == "local":
                # 如果当前套餐内余量超过此次消费
                timeDelta = endDate - startDate
            totalMinutes = math.ceil(timeDelta.total_seconds() / 60)
            print timeDelta.total_seconds()
            print totalMinutes
            if queryset[0].localBalance > totalMinutes:
                #  扣除对应套餐内余量
                queryset[0].localBalance -= totalMinutes
            else:
                #  计费并扣除余额
                queryset[0].balance -= totalMinutes * standard.objects.all()[0].localFee
                '''
    else:
        userList = []
        accountList = []
        # 打印用户信息
        userinfo = user.objects.filter(personalID=request.session['personalID'])
        for i in range(len(userinfo)):
            tmp = ""
            tmp += userinfo[i].personalID + "\n"
            tmp += userinfo[i].username + "\n"
            # tmp += userinfo[i].accountNumber + "\n"
            userList.append(tmp)
        # 打印账户信息
        accountinfo = account.objects.filter(personalID=request.session['personalID'])
        for i in range(len(accountinfo)):
            tmp = ""
            tmp += accountinfo[i].accountNumber + "\n"
            tmp += accountinfo[i].packNumber + "\n"
            tmp += accountinfo[i].accountFee + "\n"
            tmp += str(accountinfo[i].balance) + "\n"
            tmp += accountinfo[i].status + "\n"
            accountList.append(tmp)
        print "刷新完毕"
        return render(request, 'userinfo.html', {'username': request.session['username'],
                                                 'userid': request.session['personalID'],
                                                 'userList': userList,
                                                 'accountList': accountList})


def userinfo_change(request):
    if request.method == 'POST':
        form = userinfoChangeForm(request.POST)
        if form.is_valid():
            personalID = form.cleaned_data['personalID']
            username = form.cleaned_data['username']
            packNumber = form.cleaned_data['packNumber']
            # 更新用户信息
            user.objects.filter(personalID=request.session['personalID']) \
                .update(personalID=personalID, username=username)
            packlist = package.objects.filter(packNumber=packNumber)
            fee = packlist[0].packFee
            # 更新账户信息
            account.objects.filter(personalID=request.session['personalID']) \
                .update(packNumber=packNumber, accountFee=fee)

            return HttpResponse("修改成功！")
    else:
        form = userinfoChangeForm()
        return render(request, 'userinfoChange.html', {"form": form})


def stop_service(request):
    if request.method == 'POST':
        form = stopServiceForm(request.POST)
        if form.is_valid():
            accountNumber = form.cleaned_data['accountNumber']
            cancel = form.cleaned_data['cancel']
            #  print cancel
            if cancel == "yes":
                # 销号
                number.objects.get_or_create(phoneNumber=accountNumber)  # 将号码返回号码池
                account.objects.filter(accountNumber=accountNumber).delete()  # 删除账户信息
            else:
                # 停机
                account.objects.filter(accountNumber=accountNumber).update(status="disable")
            res = HttpResponse()
            res.write("<p>停机/销号成功!</p>")
            #  res.write("<button class='btn btn-default' onclick='location = '/userinfo''>进入个人信息页面</button>")
            return res
    else:
        form = stopServiceForm()
    return render(request, 'stopServiceForm.html', {"form": form})


def restore_service(request):
    if request.method == 'POST':
        form = restoreServiceForm(request.POST)
        if form.is_valid():
            # 复机
            accountNumber = form.cleaned_data['accountNumber']
            account.objects.filter(accountNumber=accountNumber).update(status="available")
            res = HttpResponse()
            res.write("<p>撤销停机成功!</p>")
            return res
    else:
        form = restoreServiceForm()
        return render(request, 'restoreService.html', {'form': form})


def checkUsage(request):
    userinfo = user.objects.filter(personalID=request.session['personalID'])
    numberList = []
    totalList = []
    if userinfo[0].userType == "user":  # 用户
        queryset = account.objects.filter(personalID=request.session['personalID'])
    else:  # 管理员
        queryset = account.objects.all()
    for i in range(len(queryset)):
        tmp = ""
        tmp += queryset[i].accountNumber + " "
        numberList.append(tmp)

    if request.method == 'POST':
        form = checkUsageForm(request.POST)
        if form.is_valid():
            accountNumber = form.cleaned_data['accountNumber']
            checkType = form.cleaned_data['checkType']
            #  print checkType
            startDate = form.cleaned_data['startDate']
            #  print startDate.year
            endDate = form.cleaned_data['endDate']
            if checkType == "traffic":
                trafficList = traffic.objects.filter(callerNumber=accountNumber,
                                                     startTime__gte=startDate,
                                                     endTime__lte=endDate)
                #  从数据库筛选处于所选中时间区域的通话记录
                for i in range((len(trafficList))):
                    tmp = ""
                    tmp += trafficList[i].callerNumber + " "
                    tmp += trafficList[i].receiverNumber + " "
                    tmp += str(trafficList[i].startTime) + " "
                    tmp += str(trafficList[i].endTime) + " "
                    tmp += trafficList[i].callType + " "
                    tmp += str(trafficList[i].fee) + " "
                    totalList.append(tmp)

            if checkType == "sms":
                smsList = sms.objects.filter(senderNumber=accountNumber,
                                             sendTime__gte=startDate,
                                             receiveTime__lte=endDate)
                for i in range(len(smsList)):
                    tmp = ""
                    tmp += smsList[i].senderNumber + " "
                    tmp += smsList[i].receiverNumber + " "
                    tmp += str(smsList[i].sendTime) + " "
                    tmp += str(smsList[i].receiveTime) + " "
                    tmp += str(smsList[i].fee) + " "
                    totalList.append(tmp)

            if checkType == "data":
                dataflowList = dataflow.objects.filter(userNumber=accountNumber,
                                                       startTime__gte=startDate,
                                                       endTime__lte=endDate)
                for i in range(len(dataflowList)):
                    tmp = ""
                    tmp += str(dataflowList[i].startTime) + " "
                    tmp += str(dataflowList[i].endTime) + " "
                    tmp += dataflowList[i].dataflow + " "
                    tmp += str(dataflowList[i].fee) + " "
                    totalList.append(tmp)

            return render(request, 'checkUsage.html',
                          {'form': form, 'numberList': numberList, 'totalList': totalList})
    else:
        form = checkUsageForm()
        return render(request, 'checkUsage.html', {'form': form, 'numberList': numberList})


def checkUserUsage(request):
    totalList = []
    if request.method == 'POST':
        form = checkUserUsageForm(request.POST)
        if form.is_valid():
            accountSet = account.objects.filter(personalID=request.session['personalID'])
            startDate = form.cleaned_data['startDate']
            endDate = form.cleaned_data['endDate']
            checkType = form.cleaned_data['checkType']
            for i in range(len(accountSet)):
                accountNumber = accountSet[i].accountNumber
                #  print accountNumber
                if checkType == "traffic":
                    trafficList = traffic.objects.filter(callerNumber=accountNumber,
                                                         startTime__gte=startDate,
                                                         endTime__lte=endDate)
                    #  从数据库筛选处于所选中时间区域的通话记录
                    print len(trafficList)
                    for j in range((len(trafficList))):
                        tmp = ""
                        tmp += trafficList[j].callerNumber + " "
                        tmp += trafficList[j].receiverNumber + " "
                        tmp += str(trafficList[j].startTime) + " "
                        tmp += str(trafficList[j].endTime) + " "
                        tmp += trafficList[j].callType + " "
                        tmp += str(trafficList[j].fee) + " "
                        totalList.append(tmp)

                if checkType == "sms":
                    smsList = sms.objects.filter(senderNumber=accountNumber,
                                                 sendTime__gte=startDate,
                                                 receiveTime__lte=endDate)
                    for j in range(len(smsList)):
                        tmp = ""
                        tmp += smsList[j].senderNumber + " "
                        tmp += smsList[j].receiverNumber + " "
                        tmp += str(smsList[j].sendTime) + " "
                        tmp += str(smsList[j].receiveTime) + " "
                        tmp += str(smsList[j].fee) + " "
                        totalList.append(tmp)

                if checkType == "data":
                    dataflowList = dataflow.objects.filter(userNumber=accountNumber,
                                                           startTime__gte=startDate,
                                                           endTime__lte=endDate)
                    for j in range(len(dataflowList)):
                        tmp = ""
                        tmp += str(dataflowList[j].startTime) + " "
                        tmp += str(dataflowList[j].endTime) + " "
                        tmp += dataflowList[j].dataflow + " "
                        tmp += str(dataflowList[j].fee) + " "
                        totalList.append(tmp)
            return render(request, 'checkUserUsage.html', {'form': form, 'totalList': totalList})

    else:
        form = checkUserUsageForm()
        return render(request, 'checkUserUsage.html', {'form': form, 'totalList': totalList})


def chargeFee(request):
    if request.method == "POST":
        form = chargeFeeForm(request.POST)
        if form.is_valid():
            accountNumber = form.cleaned_data['accountNumber']
            fee = form.cleaned_data['Fee']
            balance = account.objects.get(accountNumber=accountNumber).balance
            print balance
            account.objects.filter(accountNumber=accountNumber).update(balance=balance + fee)
            #  如果充值后余额为正数，账号恢复使用
            if account.objects.filter(accountNumber=accountNumber)[0].balance >= 0:
                account.objects.filter(accountNumber=accountNumber).update(status="available")
            return HttpResponse(" 充值成功！")
    else:
        form = chargeFeeForm()
    return render(request, 'chargeFee.html', {'form': form})


def newUsage(request):
    if request.method == "POST":
        form = NewUsageForm(request.POST)
        if form.is_valid():
            usageType = form.cleaned_data['usageType']
            startDate = form.cleaned_data['startDate']
            endDate = form.cleaned_data['endDate']
            dealerNumber = form.cleaned_data['dealerNumber']
            receiverNumber = form.cleaned_data['receiverNumber']
            callType = form.cleaned_data['callType']
            dataAmount = form.cleaned_data['amount']

            timeDelta = endDate - startDate
            totalMinutes = math.ceil(timeDelta.total_seconds() / 60)
            print timeDelta.total_seconds()
            print totalMinutes

            accountSet = account.objects.filter(accountNumber=dealerNumber)
            print accountSet[0].accountNumber
            if accountSet[0].status == "disable":
                #  当前账号已停机
                return HttpResponse("当前账号已经停机，暂不受理新话务！")
            if usageType == "traffic":
                #  当前新增话务详单
                fee = 0.0
                if callType == "local":
                    #  从套餐中扣除相应时长
                    if totalMinutes <= accountSet[0].localBalance:
                        #  当前套餐内还有余额
                        account.objects.filter(accountNumber=dealerNumber) \
                            .update(localBalance=accountSet[0].localBalance - totalMinutes)
                    else:
                        #  当前套餐余额不足本次使用，扣除余量后计费
                        totalMinutes -= account.objects.filter(accountNumber=dealerNumber)[0].localBalance
                        #  清空当前套餐余量
                        account.objects.filter(accountNumber=dealerNumber) \
                            .update(localBalance=0)
                        fee = totalMinutes * float(standard.objects.filter(id=1)[0].localFee)
                        print fee

                if callType == "remote":
                    if totalMinutes <= accountSet[0].remoteBalance:
                        #  当前套餐内还有余额
                        fee = 0.0
                        account.objects.filter(accountNumber=dealerNumber) \
                            .update(remoteBalance=accountSet[0].remoteBalance - totalMinutes)
                    else:
                        #  当前套餐余额不足本次使用，扣除余量后计费
                        totalMinutes -= account.objects.filter(accountNumber=dealerNumber)[0].remoteBalance
                        #  清空当前套餐余量
                        account.objects.filter(accountNumber=dealerNumber) \
                            .update(remoteBalance=0)
                        fee = totalMinutes * float(standard.objects.filter(id=1)[0].remoteFee)
                        print fee
                # 将计费结果写入数据库
                traffic.objects.create(callerNumber=dealerNumber,
                                       receiverNumber=receiverNumber,
                                       startTime=startDate,
                                       endTime=endDate,
                                       callType=callType,
                                       fee=fee
                                       )
                #  更新用户当前余额，并维护账号状态
                curBalance = account.objects.filter(accountNumber=dealerNumber)[0].balance
                curBalance -= fee
                account.objects.filter(accountNumber=dealerNumber).update(balance=curBalance)
                if curBalance <= 0:
                    #  余额不足，停机
                    account.objects.filter(accountNumber=dealerNumber).update(status="disable")
            if usageType == "sms":
                fee = 0.0
                if accountSet[0].smsBalance > 0:
                    #  仍有短信余量
                    tmp = accountSet[0].smsBalance
                    #  扣除余量后计费
                    account.objects.filter(accountNumber=dealerNumber).update(smsBalance=tmp - 1)
                else:
                    #  套餐内余量用光
                    fee = standard.objects.filter(id=1)[0].smsFee
                # 将计费结果写入数据库
                sms.objects.create(senderNumber=dealerNumber,
                                   receiverNumber=receiverNumber,
                                   sendTime=startDate,
                                   receiveTime=endDate,
                                   fee=fee
                                   )
                #  更新用户当前余额，并维护账号状态
                curBalance = account.objects.filter(accountNumber=dealerNumber)[0].balance
                curBalance -= fee
                account.objects.filter(accountNumber=dealerNumber).update(balance=curBalance)
                if curBalance <= 0:
                    #  余额不足，停机
                    account.objects.filter(accountNumber=dealerNumber).update(status="disable")
            if usageType == "dataflow":
                fee = 0.0
                if dataAmount <= accountSet[0].dataBalance:
                    #  当前套餐内仍有足够数据流量
                    tmp = accountSet[0].dataBalance
                    #  扣除余量后计费
                    account.objects.filter(accountNumber=dealerNumber)\
                        .update(dataBalance=tmp - dataAmount)
                else:
                    #  当前套餐余额不足本次使用，扣除余量后计费
                    dataAmount -= account.objects.filter(accountNumber=dealerNumber)[0].dataBalance
                    #  清空当前套餐余量
                    account.objects.filter(accountNumber=dealerNumber) \
                        .update(dataBalance=0)
                    fee = dataAmount * float(standard.objects.filter(id=1)[0].dataFee)
                    print fee
                # 将计费结果写入数据库
                dataflow.objects.create(userNumber=dealerNumber,
                                        startTime=startDate,
                                        endTime=endDate,
                                        dataflow=dataAmount,
                                        fee=fee
                                        )
                #  更新用户当前余额，并维护账号状态
                curBalance = account.objects.filter(accountNumber=dealerNumber)[0].balance
                curBalance -= fee
                account.objects.filter(accountNumber=dealerNumber).update(balance=curBalance)
                if curBalance <= 0:
                    #  余额不足，停机
                    account.objects.filter(accountNumber=dealerNumber).update(status="disable")
            return HttpResponse("Success!")
    else:
        form = NewUsageForm()
        return render(request, 'newUsage.html', {'form': form})
