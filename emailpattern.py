'''
dot-atom: [CFWS] dot-atom-text [CFWS]
    dot-atom-text: 1*atext *("." 1*atext)
        atext: ALPHA / DIGIT / !#$%&'*+-/=?^_`{|}~

quoted-string: [CFWS] DQUOTE *([FWS] qcontent) [FWS] DQUOTE [CFWS]
    qcontent: qtext / quoted-pair
        qtext: NO-WS-CTL / %d33 / %d35-91 / %d93-126

NO-WS-CTL: %d1-8.11.12.14-31.127
DQUOTE: "\""
CFWS: *([FWS] comment) (([FWS] comment) / FWS)
    comment: "(" *([FWS] ccontent) [FWS] ")"
        ccontent: ctext / quoted-pair / comment
            ctext: NO-WS-CTL / %d33-39 / %d42-91 / %d93-126
FWS: ([*WSP CRLF] 1*WSP)
    WSP: 
quoted-pair: ("\" text)
    text: %d1-9 / %d11 / %d12 / %d14-127

addr-spec: local-part "@" domain
    local-part: dot-atom / quoted-string
    domain: dot-atom / domain-literal
        domain-literal: [CFWS] "[" *([FWS] dcontent) [FWS] "]" [CFWS]
            dcontent: dtext / quoted-pair
                dtext: NO-WS-CTL / #non whitespace controls
                       %d33-90 / #the rest of the US-ASCII
                       %d94-126  # characters not including "[", "]", or "\"


max length 998 characters

'''


rfc2822_patterns = {}

rfc2822_patterns.update({
    'NOWSCTL': r'[\x01-\x08\x0b\x0c\x0e-\x1f\x7f]',
    'DQUOTE': '["]',
    'WSP': r'[ \t]',
    'CRLF': r'(?:\x0d\x0a)',
    'atext': r'[\w!#\$%&\'\*\+\-/=\?\^`\{\|\}~]',
    'text': r'[\x01-\x09\x0b\x0c\x0e-\x7f]',
    'comment': r'(?:?!)', #should match nothing ever
})

rfc2822_patterns.update({
    'FWS': r'(?:({WSP}*{CRLF})?{WSP}+)'.format(**rfc2822_patterns),
    'dotatomtext': r'(?:{atext}+(\.{atext}+)*)'.format(**rfc2822_patterns),
    'quotedpair': r'(?:\\{text})'.format(**rfc2822_patterns),
    'qtext': r'(?:{NOWSCTL}|[!#-\[\]-~])'.format(**rfc2822_patterns),
    'dtext': r'(?:{NOWSCTL}|[!-Z^-~])'.format(**rfc2822_patterns),
})

rfc2822_patterns.update({
    'CFWS': '{FWS}'.format(**rfc2822_patterns),
    'qcontent': r'(?:{qtext}|{quotedpair})'.format(**rfc2822_patterns),
    'dcontent': r'(?:{dtext}|{quotedpair})'.format(**rfc2822_patterns),
})

#recursive - NONONONONO
# ctext: r'(?:{NOWSCTL}|(?![\(\)\\])[\x27-\x7e])'
# ccontent: r'(?:{ctext}|{quotedpair}|{comment})'
# comment: r'\(({FWS}?{ccontent})*{FWS}\)'

rfc2822_patterns.update({
    'dotatom': r'(?:{CFWS}?{dotatomtext}{CFWS}?)'.format(**rfc2822_patterns),
    'quotedstring': r'(?:{CFWS}?"({FWS}?qcontent)*{FWS}?"{CFWS}?)'.format(**rfc2822_patterns),
    'domainliteral': r'(?:{CFWS}?\[({FWS}?{dcontent})*{FWS}?\]{CFWS}?)'.format(**rfc2822_patterns),
})

rfc2822_patterns.update({
    'domain': r'(?:{dotatom}|{domainliteral})'.format(**rfc2822_patterns),
    'localpart': r'(?:{dotatom}|{quotedstring})'.format(**rfc2822_patterns),
})

rfc2822_patterns.update({
    'addrspec': r'(?:(?P<localpart>{localpart})@(?P<domain>{domain}))'.format(**rfc2822_patterns),
})

print(rfc2822_patterns['addrspec'])
