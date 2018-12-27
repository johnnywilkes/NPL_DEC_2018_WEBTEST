# __Johnny Python's Web Test Program!__

> This document uses Markdown.  Please view on Github (https://github.com/johnnywilkes/NPL_DEC_2018_WEBTEST) or use the following for viewing: https://stackedit.io/app#

## ___Overall Program Idea___

I always start small and then refactor from there.  This means that I focused on the base challenge but thought about how to reuse code to use in the bonus challenges.  The base challenge mentioned the following error messages and therefore I knew there would probably be one test (and one function) per error message:
 - Invalid URL (syntax): Regular Expression test
 - Unknown DNS name: DNS test (used socket)
 - Unreachable IP: ICMP test (used OS/System)
 - Success: successful web call via Request
 
After creating these functions and testing the program, it wasn't hard to see that some of these functions could be reused for the bonus content (or copied and slightly modified).  This is better explained in the following flow diagram than words:

> https://github.com/johnnywilkes/NPL_DEC_2018_WEBTEST/blob/master/Flow.PNG

You can see that my strategy was to make an interactive selection menu, where the user could select the following:
```
    >>> Menu - Please select one of the following:
    >>> 1. Original Website Check
    >>> 2. IP Address Test
    >>> 3. FQDN TCp-80/443 Check
    >>> 4. QUIT
    >>> Selection: 
```

Option one is the original "base" challenge, while options two and three are the additional IP address/FQDN bonus challenges.  I considered making the http(s) status code its own menu selection, but decided that it was more of an add-on selection for the function I had to for the final web call test (Requests module).  As you can see from the flow diagram, there is a good amount of overlap between parts of code (functions) for each option of the menu.  This is the optimal setup to be more efficient and scalable in the future.


## ___Variable Naming/Program Structure___

This program uses the same variable naming, comment and program structure as last month's submission for, more information, see the section with the same name (Variable Naming/Program Structure) in the following link:
https://github.com/johnnywilkes/NPL_NOV_2018_TIME/blob/master/README.md


## ___Regular Expression___

One very important part of this program was using Regular Expression (regex) to validate an URL and/or FQDN.  Using online regex testers such as https://regex101.com made this process easier.  Originally, the challenge noted that the correct URL syntax was: http://www.server.com/object.  However, after asking the NTC for some clarification I found the following could be assumed:
 - URL can be HTTP or HTTPS.
 - We can assume for the test that "www." will be part of the domain, but it would be optimal if we had checks that didn't assume this.
 - We can assume for the test that ".com." will be part of the domain, but it would be optimal if we had checks that didn't assume this.
 - We should consider a URL with a trailing "/" to be valid.
 - Test URLs will only be one directory deep (such as http://www.server.com/object).

So again, my mantra is KISS (Keep It Simple, Stupid), so I embarked on meeting the base requirements and then improved.  Before hearing about these additional requirements, my regex could be something like:

`^http://www.\w+.\w{2,3}/\w+$` which equates to:
 - starts with `http://www.`
 - one or more word characters.
 - a single `.`.
 - two or three work characters (root domain).
 - one `\`.
 - end with one or more word characters (URI).
 
However, I had to quickly adapt to: `^https?://www.\w+.\w{2,3}/\w+/?$`
Differences are:
 - `^https?` means that http or https is allowed (`?` mean one or more of the previous character: 's')
 - The URL can end with a trailing `/` or not (the `?` again)

I had a desire to go above and beyond (without losing my mind), and realized I needed to switch to `^https?://[a-zA-Z0-9\-]*\.?[a-zA-Z0-9\-]+\.[a-zA-Z]{2,3}/[a-zA-Z0-9\-]+/?$`
 - `[a-zA-Z0-9\-]` needed to replace `\w+` because the URL parts can be a lowercase/uppercase letter, number or hyphen (except root domain which is just letters).
 - `*\.?` was needed after the section for the subdomain because it is indeed options (`*` signifies 0 or more of the previous character).

And its final form: `^https?:\/\/(?!-)[a-zA-Z0-9\-]*(?<!-)\.?(?!-)[a-zA-Z0-9\-]+(?<!-)\.[a-zA-Z]{2,3}\/(?!-)[a-zA-Z0-9\-]+(?<!-)\/?$`
 - Added negative lookaheads/lookbehinds (https://www.regular-expressions.info/lookaround.html) because even though the parts of the URL can contain hyphens, it isn't a valid URL is the sections begin or end with them.  `http://-test.com` isn't valid!
 - `(?!-)` is called a lookahead and in this case the `!` makes is a negative-lookahead meaning that it will not match if this portion of the URL starts with a hyphen.
 - `(?<!-)` is called a lookbehind and in this case the `!` makes it a negative-lookbehind meaning that it will not match if this portion of the URL ends with a hyphen.

 
## ___Possible Refactoring/Feature Releases___
 - Better Regex - mine is good but not perfect. RFC 1738, the URL standard has other definitions that the whole URL should only be so many characters in total and each FQDN/URI should only be so many characters.  Adding these would get even more complicated, so I decided to stop while I was ahead.  However, there is always room to go back and improve.
 - Ping test - the ping test I used relies on the operating system being used.  I didn't test on that many platforms (just Windows 10 and Ubuntu 16), so more testing may be needed.  Also, I think there might be better ways of doing the test (something more embedded into python).  The ping test as a whole might not be necessary, because it is more of an arbitrary check considering some websites allows http(s) but block ICMP.
 - More functionality - I think it would be good to give users the options to parse a list, text file or csv full of URLs, IPs and FQDNs to do the same checks.  The output could be sent in turn to a list, text file or csv as well.  There might be some other cool options/scenarios out there to be considered.
 - Better interactive menu - the interactive menu I have it good, but it could also be improved on.  Some type of GUI could maybe be added from Tkinter or Django, but I haven't started to look into options yet.
 
###### P.S. - Hope you like the surprise at the end!