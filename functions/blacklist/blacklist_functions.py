import re
import time
import asyncio
import ipaddress
import dns.asyncresolver

from typing import Tuple
from datetime import datetime


def updateResult(isBlacklisted, result, provider):
    if isBlacklisted:
        # add provider on top of all other providers, because it is blacklisted
        result["providers"].insert(0, provider)
        # add provider in detected_on array
        result["detected_on"].append(provider)
        result["is_blacklisted"] = True  # add is_blacklisted as True
    else:
        # add provider to providers array
        result["providers"].append(provider)


def getTemplate(ip_address: str) -> Tuple[str, str, dict]:
    # get start time of execution of code
    start_time = time.time()
    # reverse the given ip
    # requires to check blacklisted or not
    reversed_ip = ".".join(reversed(ip_address.split(".")))
    # create a format for end result
    result = {
        "detected_on": [],
        "providers": [],
        "is_blacklisted": False,
        "hostname": ip_address,
        "date": str(datetime.now())[:19],
    }

    return start_time, reversed_ip, result


# from providers_data import providers
async def check_dnsbl(reversed_ip: str, provider: str) -> Tuple[bool, str]:
    query = f"{reversed_ip}.{provider}"  # query for resolver.resolve concated the reversed ip with provider with "."
    resolver = dns.asyncresolver.Resolver()  # resolver object from dns

    try:
        answer = await resolver.resolve(query)  # get answer from resolver
        return True, provider
    # if error while resolving query
    # all should return Tuple as (False, provider)
    except dns.resolver.NXDOMAIN:
        return False, provider
    except dns.resolver.NoAnswer:
        return False, provider
    except dns.resolver.Timeout:
        return False, provider
    except dns.resolver.NoNameservers:
        return False, provider


async def check_dnsbl_providers(ip_address: str, providers: list) -> dict:
    start_time, reversed_ip, result = getTemplate(ip_address)

    # add task to tasks queue
    # add task for each provider in providers list
    tasks = [check_dnsbl(reversed_ip, provider["provider"]) for provider in providers]

    responses = await asyncio.gather(*tasks)  # wait for all tasks to complete

    # each response has a chck, resp and provider on which it is checked
    for isBlacklisted, checked_provider in responses:
        updateResult(isBlacklisted, result, checked_provider)

    # get start time of execution of code
    end_time = time.time()
    # total time of code execution
    result["time_elapsed"] = round(end_time - start_time, 2)
    # return result
    return result


# function to check is ip is valid or not based on regex pattern
def is_valid_ipv4(ip):
    ipv4_regex = re.compile(
        r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    )
    return re.match(ipv4_regex, ip) is not None


# function to get ips in between two ips including both
def ips_between(start_ip: str, end_ip: str) -> list:
    start_ip_obj = ipaddress.IPv4Address(start_ip)  # get the ip object for start ip
    end_ip_obj = ipaddress.IPv4Address(end_ip)  # get the ip object for end ip

    # start ip should be less than end ip, if not then raise error
    if start_ip_obj > end_ip_obj:
        raise ValueError("Start IP should be less than or equal to End IP")

    return [
        str(ipaddress.IPv4Address(ip))  # convert to string for each ip
        # in range(a,b), last ip is ignored so added 1 in it
        for ip in range(int(start_ip_obj), int(end_ip_obj) + 1)
    ]
