# coding=utf-8
from django import forms


class registerForm(forms.Form):
    personalID = forms.CharField(label="身份证号码", max_length=20, widget=forms.NumberInput)
    username = forms.CharField(label="客户名", max_length=20, widget=forms.TextInput)
    # accountNumber


class loginForm(forms.Form):
    personalID = forms.CharField(label="身份证号码", max_length=20, widget=forms.NumberInput)
    username = forms.CharField(label="客户名", max_length=20, widget=forms.TextInput)


class createAccountForm(forms.Form):
    packNumber = forms.IntegerField(label="选择套餐代码", widget=forms.NumberInput)
    chargeFee = forms.IntegerField(label="预存话费数量", widget=forms.NumberInput)
    phoneNumber = forms.IntegerField(label="预选号码", widget=forms.NumberInput)


class userinfoChangeForm(forms.Form):
    personalID = forms.CharField(label="身份证号码", max_length=20, widget=forms.NumberInput)
    username = forms.CharField(label="客户名", max_length=20, widget=forms.TextInput)
    packNumber = forms.IntegerField(label="修改套餐代码", widget=forms.NumberInput)


class stopServiceForm(forms.Form):
    accountNumber = forms.IntegerField(label="停机号码", widget=forms.NumberInput)
    cancel = forms.ChoiceField(label="是否销号？", required=True,
                               choices=(("yes", "是"), ("no", "否")), widget=forms.RadioSelect)


class chargeFeeForm(forms.Form):
    accountNumber = forms.IntegerField(label="充值号码", widget=forms.NumberInput)
    Fee = forms.FloatField(label="充值金额", widget=forms.NumberInput)


class restoreServiceForm(forms.Form):
    accountNumber = forms.IntegerField(label="撤销停机号码", widget=forms.NumberInput)


class checkUsageForm(forms.Form):
    accountNumber = forms.IntegerField(label="请输入待查询的号码",
                                       # id="accountNumber",
                                       widget=forms.NumberInput)
    '''
    checkall = forms.ChoiceField(label="查询所有账号详单",
                                 # id="checkall",
                                 choices=(('yes', '是'), ('no', '否')),
                                 widget=forms.RadioSelect)
                                 '''
    startDate = forms.DateTimeField(label="查询起始时间", widget=forms.SelectDateWidget)
    endDate = forms.DateTimeField(label="查询终止时间", widget=forms.SelectDateWidget)
    checkType = forms.ChoiceField(label="查询类别",
                                  choices=(('traffic', '话务'),
                                           ('sms', '短信'),
                                           ('data', '数据流量')))


class checkUserUsageForm(forms.Form):
    startDate = forms.DateTimeField(label="查询起始时间", widget=forms.SelectDateWidget)
    endDate = forms.DateTimeField(label="查询终止时间", widget=forms.SelectDateWidget)
    checkType = forms.ChoiceField(label="查询类别",
                                  choices=(('traffic', '话务'),
                                           ('sms', '短信'),
                                           ('data', '数据流量')))


class NewUsageForm(forms.Form):
    usageType = forms.ChoiceField(label="类别",
                                  choices=(('traffic', '话务'),
                                           ('sms', '短信'),
                                           ('dataflow', '数据流量')))
    startDate = forms.DateTimeField(label="起始时间",
                                    help_text="(yyyy-mm-dd hh:mm:ss)",
                                    widget=forms.DateTimeInput)
    endDate = forms.DateTimeField(label="终止时间",
                                  help_text="(yyyy-mm-dd hh:mm:ss)",
                                  widget=forms.DateTimeInput)
    dealerNumber = forms.IntegerField(label="发起者账号",
                                        widget=forms.NumberInput)
    receiverNumber = forms.IntegerField(label="接收者账号（数据流量类型为空）",
                                        widget=forms.NumberInput, required=False)
    callType = forms.ChoiceField(label="呼叫类型",
                                 choices=(('local', '本地通话'),
                                          ('remote', '长途通话')),
                                 required=False)
    amount = forms.FloatField(label="数据流量", widget=forms.NumberInput, required=False)
