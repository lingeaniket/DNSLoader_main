providers = [
    {"provider": "all.s5h.net", "categories": ["unknown"]},
    {"provider": "aspews.ext.sorbs.net", "categories": ["unknown"]},
    {"provider": "b.barracudacentral.org", "categories": ["spam"]},  # for bulk Check
    {"provider": "bl.nordspam.com", "categories": ["spam"]},
    {"provider": "blackholes.five-ten-sg.com", "categories": ["spam", "malware"]},
    {"provider": "bl.spamcop.net", "categories": ["spam"]},  # for bulk Check
    {"provider": "dnsbl.sorbs.net", "categories": ["spam"]},  # for bulk Check
    {"provider": "dnsbl-1.uceprotect.net", "categories": ["spam"]},
    {"provider": "dnsbl-2.uceprotect.net", "categories": ["botnet"]},
    {"provider": "dnsbl-3.uceprotect.net", "categories": ["botnet", "malware"]},
    {"provider": "dul.dnsbl.sorbs.net", "categories": ["dynamic IP"]},
    {
        "provider": "zen.spamhaus.org",
        "categories": ["spam"],
    },
    {"provider": "psbl.surriel.com", "categories": ["spam"]},
    {"provider": "virbl.dnsbl.bit.nl", "categories": ["virus"]},
    {"provider": "rbl.spamrl.com", "categories": ["spam", "phishing"]},
    {"provider": "spam.dnsbl.anonmails.de", "categories": ["spam"]},
    {"provider": "cbl.abuseat.org", "categories": ["botnet", "malware"]},
    {"provider": "multi.surbl.org", "categories": ["spam"]},
    {"provider": "dnsbl-0.junkemailfilter.com", "categories": ["spam"]},
    {"provider": "dnsbl.abuse.ch", "categories": ["botnet"]},
    {"provider": "dnsbl.justspam.org", "categories": ["spam"]},
    {"provider": "dnsbl.madavi.de", "categories": ["spam"]},
    {"provider": "dnsbl.manitu.net", "categories": ["spam"]},
    {"provider": "dnsbl.proxybl.org", "categories": ["proxy"]},
    {"provider": "dnsbl.rv-soft.info", "categories": ["unknown"]},
    {"provider": "dnsbl.tornevall.org", "categories": ["spam"]},
    {"provider": "babl.rbl.webiron.net", "categories": ["botnet"]},
    {"provider": "bl.blocklist.de", "categories": ["malware"]},
    {"provider": "ubl.unsubscore.com", "categories": ["spam"]},
    {"provider": "access.redhawk.org", "categories": ["unknown"]},
    {"provider": "relays.bl.gweep.ca", "categories": ["spam"]},
    {"provider": "relays.bl.kundenserver.de", "categories": ["spam"]},
    {"provider": "relays.nether.net", "categories": ["spam"]},
    {"provider": "sbl.spamhaus.org", "categories": ["spam"]},
    {"provider": "ubl.lashback.com", "categories": ["unsubscribe"]},
    {"provider": "dnsbl.rizon.net", "categories": ["spam"]},
    {"provider": "rbl.efnetrbl.org", "categories": ["spam"]},
    {"provider": "spamsources.fabel.dk", "categories": ["spam"]},
    {"provider": "ubl.spamhaus.org", "categories": ["spam"]},
    {"provider": "cblless.anti-spam.org.cn", "categories": ["spam"]},
    {"provider": "dnsbl.kempt.net", "categories": ["spam"]},
    {"provider": "dnsblchile.org", "categories": ["spam"]},
    {"provider": "dnsbl.inps.de", "categories": ["spam"]},
    {"provider": "drone.abuse.ch", "categories": ["malware"]},
    {"provider": "dyna.spamrats.com", "categories": ["dynamic IP"]},
    {"provider": "rbl.interserver.net", "categories": ["spam"]},
    {"provider": "korea.services.net", "categories": ["geolocation"]},
    {"provider": "netblock.pedantic.org", "categories": ["spam"]},
    {"provider": "spamguard.leadmon.net", "categories": ["spam"]},
    {"provider": "tor.dan.me.uk", "categories": ["proxy"]},
    {"provider": "torexit.dan.me.uk", "categories": ["proxy"]},
    {"provider": "rbl.orbitrbl.com", "categories": ["spam"]},
    {"provider": "ubl.nszones.com", "categories": ["spam"]},
    {"provider": "dnsbl.spamrats.com", "categories": ["spam"]},
    {"provider": "dyn.nszones.com", "categories": ["dynamic IP"]},
    {"provider": "rbl.realtimeblacklist.com", "categories": ["spam"]},
    {"provider": "safe.dnsbl.sorbs.net", "categories": ["spam"]},
    {"provider": "spam.abuse.ch", "categories": ["spam"]},
    {"provider": "truncate.gbudb.net", "categories": ["spam"]},
    {"provider": "rbl.abuse.ro", "categories": ["spam"]},
    {"provider": "bl.mailspike.net", "categories": ["spam"]},
    {"provider": "bogons.cymru.com", "categories": ["bogon IP"]},
    {"provider": "dnsbl.cyberlogic.net", "categories": ["spam"]},
    {"provider": "srn.surgate.net", "categories": ["spam"]},
    {"provider": "bl.spamcannibal.org", "categories": ["spam"]},
    {"provider": "ip.v4bl.org", "categories": ["spam"]},
    {"provider": "shorturl.abuse.ch", "categories": ["malware"]},
    {"provider": "wormrbl.imp.ch", "categories": ["malware"]},
    {"provider": "rbl.efnet.org", "categories": ["spam"]},
    {"provider": "blacklist.woody.ch", "categories": ["spam"]},
    {"provider": "dnsbl.dronebl.org", "categories": ["botnet", "proxy"]},
    {"provider": "ubl.fusionzero.com", "categories": ["spam"]},
    {"provider": "fnrbl.fast.net", "categories": ["spam"]},
    {"provider": "pofon.foobar.hu", "categories": ["spam"]},
    {"provider": "spam.rbl.blockedservers.com", "categories": ["spam"]},
    {"provider": "rbl.suresupport.com", "categories": ["spam"]},
    {"provider": "spam.dnsbl.anonmails.de", "categories": ["spam"]},
    {"provider": "blacklist.sci.kun.nl", "categories": ["spam"]},
    {"provider": "rbl.lugh.ch", "categories": ["spam"]},
]

# for bulk Check
providers_bulk = [
    {
        "provider": "zen.spamhaus.org",
        "categories": ["spam", "malware", "botnet"],
    },
    {"provider": "b.barracudacentral.org", "categories": ["spam"]},
    {"provider": "bl.spamcop.net", "categories": ["spam"]},
]