date_patterns = {
		"%Y%m%d": "^\\d{8}$",
		"%m/%d/%y": "^\\d{1,2}(/)\\d{1,2}(/)\\d{2}$",
		"%d-%m-%Y": "^\\d{1,2}-\\d{1,2}-\\d{4}$",
		"%d/%m/%Y": "^\\d{1,2}(/)\\d{1,2}(/)\\d{4}$",
		"%Y-%m-%d": "^\\d{4}-\\d{1,2}-\\d{1,2}$",
        "%m/%d/%Y": "^(1[0-2]|0[1-9])/(3[01]|[12][0-9]|0[1-9])/[0-9]{4}$",
        "%m-%d-%Y": "^(1[0-2]|0[1-9])-(3[01]|[12][0-9]|0[1-9])-[0-9]{4}$",
        "%Y/%m/%d": "^\\d{4}/\\d{1,2}/\\d{1,2}$",
        "%d %b %Y": "^\\d{1,2}\\s[a-z]{3}\\s\\d{4}$",
        "%d-%b-%Y": "^\\d{1,2}-[a-z]{3}-\\d{4}$",
        "%d %B %Y": "^\\d{1,2}\\s[a-z]{4,}\\s\\d{4}$",
        "%b, %d %Y": "^[a-z]{3,},\\s\\d{1,2}\\s\\d{4}$",
        "%b %d, %Y": "^[a-z]{3,}\\s\\d{1,2},\\s\\d{4}$",
        "%Y%m%d%H%M": "^\\d{12}$",
        "%Y%m%d %H%M": "^\\d{8}\\s\\d{4}$",
        "%d-%m-%Y %H:%M": "^\\d{1,2}-\\d{1,2}-\\d{4}\\s\\d{1,2}:\\d{2}$",
        "%Y-%m-%d %H:%M": "^\\d{4}-\\d{1,2}-\\d{1,2}\\s\\d{1,2}:\\d{2}$",
        "%m/%d/%Y %H:%M": "^\\d{1,2}/\\d{1,2}/\\d{4}\\s\\d{1,2}:\\d{2}$",
        "%Y/%m/%d %H:%M": "^\\d{4}/\\d{1,2}/\\d{1,2}\\s\\d{1,2}:\\d{2}$",
        "%d %b %Y %H:%M": "^\\d{1,2}\\s[a-z]{3}\\s\\d{4}\\s\\d{1,2}:\\d{2}$",
        "%d %B %Y %H:%M": "^\\d{1,2}\\s[a-z]{4,}\\s\\d{4}\\s\\d{1,2}:\\d{2}$",
        "%Y%m%d%H%M%S": "^\\d{14}$",
        "%Y%m%d %H%M%S": "^\\d{8}\\s\\d{6}$",
        "%d-%m-%Y %H:%M:%S": "^\\d{1,2}-\\d{1,2}-\\d{4}\\s\\d{1,2}:\\d{2}:\\d{2}$",
        "%Y-%m-%d %H:%M:%S": "^\\d{4}-\\d{1,2}-\\d{1,2}\\s\\d{1,2}:\\d{2}:\\d{2}$",
        "%m/%d/%Y %H:%M:%S": "^\\d{1,2}/\\d{1,2}/\\d{4}\\s\\d{1,2}:\\d{2}:\\d{2}$",
        "%Y/%m/%d %H:%M:%S": "^\\d{4}/\\d{1,2}/\\d{1,2}\\s\\d{1,2}:\\d{2}:\\d{2}$",
        "%d %b %Y %H:%M:%S": "^\\d{1,2}\\s[a-z]{3}\\s\\d{4}\\s\\d{1,2}:\\d{2}:\\d{2}$",
        "%d %B %Y %H:%M:%S": "^\\d{1,2}\\s[a-z]{4,}\\s\\d{4}\\s\\d{1,2}:\\d{2}:\\d{2}$",
        "%b %d %Y": "^[a-z]{3,}\\s\\d{1,2}\\s\\d{4}$",
        "%d %m %Y": "^d{1,2}\\s\\[a-z]{3,}\\s\\d{4}$",
        "%d%m%y": "^\\d{2}\\d{2}\\d{2}$",
        "%m%d%y": "^\\d{2}\\d{2}\\d{2}$",
        "%m-%d-%y": "^\\d{1,2}-\\d{1,2}-\\d{2}$",
        "%d-%m-%y": "^\\d{2}-\\d{2}-\\d{2}$",
        "%B %Y": "^[a-zA-Z]+\\s\\d{4}$",
        "%d-%b-%y":"^\\d{1,2}-[a-z]{3}-\\d{2}$",
        "%d-%B-%Y":"^\\d{1,2}-[a-zA-Z]+-\\d{4}$"
}
