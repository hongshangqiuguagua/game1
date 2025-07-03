"""
示例数据

包含应用初始化时使用的示例数据
"""

from typing import Dict, List, Any

def get_admin_user() -> Dict[str, str]:
    """
    返回默认管理员用户信息
    """
    return {
        "username": "admin",
        "email": "admin@example.com", 
        "password": "adminpassword"
    }


def get_sample_levels() -> List[Dict[str, Any]]:
    """
    返回示例关卡数据，包括邮件
    """
    return [
        {
            "name": "初级挑战",
            "description": "学习识别具有明显特征的钓鱼邮件。",
            "order": 1,
            "trick_summary": "初级挑战主要关注最常见的钓鱼邮件特征：包括可疑的发件人地址（例如拼写错误）、含有紧急或威胁性语言的邮件主题、以及正文中要求点击可疑链接或提供个人信息的行为。请务必对这些信号保持警惕。",
            "emails": [
                {
                    "sender": "security@g00gle.com",
                    "subject": "您的账户已被锁定",
                    "content": "尊敬的用户，\n\n我们检测到您的账户存在异常活动，为了保护您的账户安全，我们已暂时锁定您的账户。\n\n请点击以下链接重新验证您的身份信息：\n[重新验证](http://fake-google.com/verify)\n\n如不立即处理，您的账户将在24小时内被永久锁定。\n\n谷歌安全团队",
                    "is_phishing": True,
                    "phishing_clue": "发件人域名拼写错误：g00gle.com（正确应为google.com），且链接指向可疑网站。"
                },
                {
                    "sender": "newsletter@company.com",
                    "subject": "本周新闻简报",
                    "content": "尊敬的用户，\n\n感谢您订阅我们的周报。以下是本周的热门新闻：\n\n1. 公司推出新产品\n2. 行业动态分析\n3. 用户反馈调查\n\n如果您有任何问题，请回复此邮件。\n\n祝好，\n公司团队",
                    "is_phishing": False
                }
            ]
        },
        {
            "name": "中级挑战",
            "description": "识别伪装得更好的钓鱼邮件。",
            "order": 2,
            "trick_summary": "中级挑战的邮件伪装得更巧妙。您需要注意的不仅是拼写错误，更要关注邮件的整体\"语气\"是否专业、链接的真实指向（鼠标悬停查看）、以及那些利用贪婪或恐惧心理（如中奖、账户风险）诱骗您采取行动的企图。",
            "emails": [
                {
                    "sender": "support@microsft.com",
                    "subject": "您的Microsoft账户需要更新",
                    "content": "尊敬的客户，\n\n为了符合我们新的安全政策，所有用户必须更新其账户信息。请访问我们的安全门户网站更新您的信息：\n[更新链接](http://microsft-security-portal.com)\n\n感谢您的合作。\n\nMicrosoft 支持",
                    "is_phishing": True,
                    "phishing_clue": "发件人域名拼写错误：microsft.com（正确应为microsoft.com），利用安全策略更新为借口诱导点击。"
                },
                {
                    "sender": "orders@amazon.com",
                    "subject": "您的Amazon订单确认 #123-4567890",
                    "content": "您好，\n\n感谢您在Amazon的购物！您的订单 #123-4567890 已确认，预计将在3-5个工作日内送达。\n\n您可以随时查看订单状态：[查看订单](https://www.amazon.com/orders)\n\n谢谢！",
                    "is_phishing": False
                }
            ]
        },
        {
            "name": "高级挑战",
            "description": "面对模仿得惟妙惟肖的钓鱼邮件。",
            "order": 3,
            "trick_summary": "高级挑战中的钓鱼邮件几乎与真实邮件无异。关键在于细节：发件人邮箱的细微差别、邮件中是否存在官方渠道从未提及的\"新流程\"、以及邮件页脚的版权信息是否完整正确。在处理这类邮件时，最佳策略是通过官方网站或应用核实，而不是直接点击邮件中的任何内容。",
            "emails": [
                {
                    "sender": "paypal-service@paypa1.com",
                    "subject": "您的账户需要验证",
                    "content": "尊敬的用户，\n\n我们检测到您的账户最近有一些可疑活动。为了确保您的账户安全，我们需要您验证您的身份。\n\n请点击下方链接进行账户验证：\n[验证我的账户](https://secure-paypal.verification-center.com)\n\n如果您未在48小时内完成此操作，您的账户可能会被限制使用。\n\nPayPal 安全团队\n© 2023 PayPal, Inc. 保留所有权利。",
                    "is_phishing": True,
                    "phishing_clue": "发件人域名中的字母'l'被数字'1'替换（paypa1而不是paypal）；链接指向非官方域名，不是paypal.com。"
                },
                {
                    "sender": "account-security@apple.com",
                    "subject": "您的Apple ID已在新设备上登录",
                    "content": "尊敬的Apple用户，\n\n您的Apple ID刚刚在一台新的iPhone设备上登录。\n\n设备型号：iPhone 13 Pro\n登录时间：2023年8月15日 14:30\n位置：北京, 中国\n\n如果这不是您本人操作，请立即点击以下链接保护您的账户：\n[保护我的账户](https://appleid-verify.com/secure)\n\n此致，\nApple 安全团队",
                    "is_phishing": True,
                    "phishing_clue": "虽然发件人域名看起来正确，但链接指向非苹果官方域名(appleid-verify.com)。苹果公司不会通过邮件中的链接要求您处理安全问题，而是要求您直接访问appleid.apple.com。"
                },
                {
                    "sender": "support@dropbox.com",
                    "subject": "您的共享文档已更新",
                    "content": "您好，\n\n您的团队成员已更新共享文档。\n\n文档名称：Q3财务报告.docx\n更新时间：2023年9月15日 10:45\n\n[查看更新](https://www.dropbox.com/documents/shared/finance)\n\n如果您无法访问该链接，请复制以下网址到浏览器地址栏：\nhttps://www.dropbox.com/documents/shared/finance\n\nDropbox 团队\n© 2023 Dropbox, Inc., 所有权利保留。",
                    "is_phishing": False
                }
            ]
        },
        {
            "name": "专家挑战",
            "description": "识别最顶级的、以假乱真的钓鱼攻击。",
            "order": 4,
            "trick_summary": "专家挑战模拟的是具有针对性的\"鱼叉式\"攻击。这类邮件可能包含您的真实姓名或相关信息，迷惑性极强。识别关键在于\"来源核实\"：即使邮件看起来完全正常，如果它要求您执行敏感操作（如修改密码、转账），请务必通过一个完全独立的、您信任的渠道（如官方APP、浏览器收藏夹的官网链接）来验证其真实性，而不是信任邮件本身。",
            "emails": [
                {
                    "sender": "hr@your-company.com",
                    "subject": "员工福利政策更新 - 需要确认",
                    "content": "亲爱的员工，\n\n我们公司最近更新了员工福利政策。为确保您能享受全部福利，请在系统中确认您已阅读新政策。\n\n请使用您的公司账号登录以下链接确认：\n[确认政策更新](https://hr-portal.your-company-verify.com)\n\n如有任何问题，请回复此邮件或联系HR部门。\n\n祝好，\n人力资源部",
                    "is_phishing": True,
                    "phishing_clue": "虽然发件人地址与公司域名匹配，但链接域名与公司官方域名不同(your-company-verify.com而不是your-company.com)。这是一种高级的\"鱼叉式\"钓鱼攻击，针对特定公司员工。"
                },
                {
                    "sender": "security-alerts@gmail.com",
                    "subject": "Google安全警报 - 账户恢复选项已更新",
                    "content": "您好，\n\n我们检测到您的Google账户的恢复电子邮件地址已被更改。\n\n更改时间: 2023年10月12日 18:23 (UTC+8)\n使用的设备: Windows PC\n大致位置: 上海, 中国\n\n如果这是您进行的更改，则无需任何操作。\n\n如果这不是您进行的操作，请尽快登录您的Google账户并审核您的安全设置: https://myaccount.google.com/security\n\nGoogle账户团队",
                    "is_phishing": False
                },
                {
                    "sender": "customercare@bank-of-china.secure-login.com",
                    "subject": "【重要】您的银行账户安全警告",
                    "content": "尊敬的客户：\n\n我们检测到您的账户存在异常登录尝试，为保障您的账户安全，请立即验证您的身份信息。\n\n请点击以下链接进入安全验证页面：\n[验证身份](https://secure-login.com/bank-of-china/verify)\n\n如不是您本人操作，请忽略此邮件并联系我们的客服热线：400-888-8888\n\n中国银行 客户服务中心",
                    "is_phishing": True,
                    "phishing_clue": "发件人地址使用了复合域名(bank-of-china.secure-login.com)而不是官方域名(boc.cn)，这是一种高级的域名伪装技术。正规银行绝不会通过邮件链接要求验证身份信息。"
                }
            ]
        },
        {
            "name": "社交媒体钓鱼挑战",
            "description": "识别针对社交媒体和流行应用的钓鱼攻击。",
            "order": 5,
            "trick_summary": "社交媒体钓鱼攻击利用人们对流行平台的信任，通常模仿通知、好友请求或热门活动。这类攻击尤其危险，因为社交媒体账号往往关联了我们的个人信息、社交圈和其他账号。请特别注意任何要求您重新登录、验证账号或参与异常优惠活动的邮件，并养成直接通过官方应用检查通知的习惯。",
            "emails": [
                {
                    "sender": "notifications@wechat-security.com",
                    "subject": "【微信安全中心】您的账号存在异常登录",
                    "content": "亲爱的微信用户：\n\n我们检测到您的微信账号于2023年11月28日在一个新设备上登录，该设备位于广州。\n\n如果这不是您本人操作，您的账号可能已被盗用。请立即点击下方链接重置密码：\n[重置密码](https://wechat-account-verify.com/reset)\n\n为保障您的账号安全，请在24小时内完成验证。\n\n微信安全团队",
                    "is_phishing": True,
                    "phishing_clue": "微信官方不会通过邮件发送账号安全通知，且发件人域名'wechat-security.com'并非微信官方域名。正规的微信安全通知会直接在应用内推送。"
                },
                {
                    "sender": "no-reply@douyin.com",
                    "subject": "您的抖音视频获得官方推荐",
                    "content": "恭喜您！\n\n您最近上传的视频《生活小妙招》已被抖音官方推荐，并有机会获得流量扶持。\n\n为了确保您能获得推荐流量和相关收益，请在24小时内完成创作者身份验证：\n[完成验证](https://douyin-creator-verify.net)\n\n感谢您对抖音平台的支持！\n\n抖音创作者中心",
                    "is_phishing": True,
                    "phishing_clue": "虽然发件人看似来自抖音官方，但链接域名'douyin-creator-verify.net'并非官方域名。抖音官方通知会在应用内发送，不会要求通过外部链接验证身份。"
                },
                {
                    "sender": "security@accounts.tiktok.com",
                    "subject": "TikTok Security: New Login Alert",
                    "content": "Hi TikTok User,\n\nWe noticed a new login to your TikTok account from a device in Singapore on November 27, 2023.\n\nDevice: iPhone 14\nLocation: Singapore\nTime: 15:42 SGT\n\nIf this wasn't you, please secure your account immediately by clicking here: https://www.tiktok.com/account/security\n\nIf this was you, you can ignore this message.\n\nTikTok Security Team",
                    "is_phishing": False
                },
                {
                    "sender": "team@linkedin-mail.com",
                    "subject": "您有5条未读消息和3个新的职位推荐",
                    "content": "您好，\n\n您的LinkedIn账号有以下更新：\n- 5条未读消息\n- 3个与您技能匹配的新职位\n- 8位新用户查看了您的简历\n\n查看详情并回复消息，请点击此处：\n[查看LinkedIn更新](https://linkedin-profile-view.com/secure/messages)\n\n保持联系对您的职业发展至关重要！\n\nLinkedIn专业团队",
                    "is_phishing": True,
                    "phishing_clue": "发件人域名'linkedin-mail.com'不是LinkedIn官方使用的域名，官方应为'linkedin.com'或'email.linkedin.com'。链接也指向非官方网站'linkedin-profile-view.com'。"
                },
                {
                    "sender": "noreply@instagram.email",
                    "subject": "Instagram: 您的账号已被举报违规",
                    "content": "尊敬的Instagram用户，\n\n我们收到多个关于您账号违反社区准则的举报。您的账号面临被永久禁用的风险。\n\n如果您认为这是一个错误，请在48小时内通过以下链接提交申诉：\n[提交申诉](https://instagram-appeal-center.com)\n\n如不及时处理，您的账号将被永久删除。\n\nInstagram支持团队",
                    "is_phishing": True,
                    "phishing_clue": "Instagram官方不会通过这种方式通知账号违规，且发件人域名和申诉链接都不是官方域名。此类邮件利用用户对账号被封的恐惧心理诱导点击。"
                },
                {
                    "sender": "info@xiaohongshu.com",
                    "subject": "恭喜您获得小红书品牌合作机会",
                    "content": "亲爱的小红书创作者，\n\n恭喜您！基于您的优质内容表现，您已被选中参与我们的品牌合作计划。\n\n一家知名化妆品品牌希望与您合作推广其新产品系列，预算为¥8,000-15,000。\n\n请点击以下链接查看详情并确认您的参与：\n[查看合作详情](https://xiaohongshu-brands.com/collab/register)\n\n请在3天内确认，逾期名额将让给其他创作者。\n\n小红书品牌合作团队",
                    "is_phishing": True,
                    "phishing_clue": "虽然邮件主题非常诱人，但发件人域名虽然看似官方，链接却指向非官方网站'xiaohongshu-brands.com'。小红书官方合作邀请会通过应用内私信或官方认证的电子邮件发送，且不会要求通过可疑链接注册。"
                },
                {
                    "sender": "no-reply@zhihu.com",
                    "subject": "知乎：您的回答获得官方推荐",
                    "content": "尊敬的知乎用户，\n\n恭喜您！您对问题《如何提高工作效率？》的回答因专业性和帮助性突出，已被选为官方推荐回答。\n\n您的回答已获得：\n- 5,243次浏览\n- 1,876次点赞\n- 官方推荐标记\n\n查看详情并领取创作者激励金，请登录您的知乎账号：\n[查看我的回答](https://www.zhihu.com/answer/detail)\n\n感谢您为知乎社区做出的贡献！\n\n知乎团队",
                    "is_phishing": False
                },
                {
                    "sender": "support@bilibili.secure-account.com",
                    "subject": "【哔哩哔哩】您的账号可能存在安全风险",
                    "content": "亲爱的哔哩哔哩用户：\n\n我们的系统检测到您的账号近期存在异常登录行为，可能已被他人获取。为保障您的账号安全和虚拟财产不受损失，请立即验证您的身份并修改密码。\n\n请通过以下链接进行身份验证：\n[立即验证](https://bilibili-account-protect.com/verify)\n\n如果您忽略此警告，您的账号可能被限制使用，您的会员状态和硬币余额可能受到影响。\n\n哔哩哔哩安全中心",
                    "is_phishing": True,
                    "phishing_clue": "发件人域名'bilibili.secure-account.com'是一个伪造域名，不是B站官方域名。B站官方安全通知会在APP内推送，不会要求用户通过邮件链接验证身份。"
                }
            ]
        }
    ] 