'''
address     =  mailbox                      ; one addressee
            /  group                        ; named list

group       =  phrase ":" [#mailbox] ";"

mailbox     =  addr-spec                    ; simple address
            /  phrase route-addr            ; name & addr-spec

route-addr  =  "<" [route] addr-spec ">"

route       =  1#("@" domain) ":"           ; path-relative

addr-spec   =  local-part "@" domain        ; global address

local-part  =  word *("." word)             ; uninterpreted
                                            ; case-preserved

domain      =  sub-domain *("." sub-domain)

sub-domain  =  domain-ref / domain-literal

domain-ref  =  atom                         ; symbolic reference


                                            ; (  Octal, Decimal.)
CHAR        =  <any ASCII character>        ; (  0-177,  0.-127.)
ALPHA       =  <any ASCII alphabetic character>
                                            ; (101-132, 65.- 90.)
                                            ; (141-172, 97.-122.)
DIGIT       =  <any ASCII decimal digit>    ; ( 60- 71, 48.- 57.)
CTL         =  <any ASCII control           ; (  0- 37,  0.- 31.)
                character and DEL>          ; (    177,     127.)
CR          =  <ASCII CR, carriage return>  ; (     15,      13.)
LF          =  <ASCII LF, linefeed>         ; (     12,      10.)
SPACE       =  <ASCII SP, space>            ; (     40,      32.)
HTAB        =  <ASCII HT, horizontal-tab>   ; (     11,       9.)
<">         =  <ASCII quote mark>           ; (     42,      34.)
CRLF        =  CR LF

LWSP-char   =  SPACE / HTAB                 ; semantics = SPACE

linear-white-space =  1*([CRLF] LWSP-char)  ; semantics = SPACE
                                            ; CRLF => folding

specials    =  "(" / ")" / "<" / ">" / "@"  ; Must be in quoted-
            /  "," / ";" / ":" / "\" / <">  ;  string, to use
            /  "." / "[" / "]"              ;  within a word.

delimiters  =  specials / linear-white-space / comment

text        =  <any CHAR, including bare    ; => atoms, specials,
                CR & bare LF, but NOT       ;  comments and
                including CRLF>             ;  quoted-strings are
                                            ;  NOT recognized.

atom        =  1*<any CHAR except specials, SPACE and CTLs>

quoted-string = <"> *(qtext/quoted-pair) <">; Regular qtext or
                                            ;   quoted chars.

qtext       =  <any CHAR excepting <">,     ; => may be folded
                "\" & CR, and including
                linear-white-space>

domain-literal =  "[" *(dtext / quoted-pair) "]"


dtext       =  <any CHAR excluding "[",     ; => may be folded
                "]", "\" & CR, & including
                linear-white-space>

comment     =  "(" *(ctext / quoted-pair / comment) ")"

ctext       =  <any CHAR excluding "(",     ; => may be folded
                ")", "\" & CR, & including
                linear-white-space>

quoted-pair =  "\" CHAR                     ; may quote any char

phrase      =  1*word                       ; Sequence of words

word        =  atom / quoted-string
'''

#address = r'(?:{mailbox}|{group})' #unused - mailbox is what I want
#group = r'(?:{phrase}:(?:{mailbox(?:,{mailbox})*})?;)' #unused - mailbox is what I want

mailbox = r'(?:{addrspec}|{phrase}{routeaddr})'
routeaddr = r'(?:<{route}{addrspec}>)'
route = r'(?:{domain}(?:,{domain})*:)'
addrspec = r'(?:{localpart}@{domain})'
localpart = r'(?:{word}(?:\.{word})*)'
domain = r'(?:{subdomain}(?:\.{subdomain})*)'
subdomain = r'(?:{domainref}|{domainliteral})'
domainref = r'{atom}'

word = r'(:{atom}|{quotedstring})'
atom = r'(?:[^\(\)<>@,;:\\"\.\[\] \x00-\x1f\x7f]+)'
quotedstring = r'(?:"(?:{qtext}|quotedpair)*")'
qtext = r'(?:[^"\\\x0d])'
linearwhitespace = r'(?:(?:{CRLF}?{LWSPchar})+)'
CRLF = r'[\x0d\x0a]'
LWSPchar = r'[ \t]'
quotedpair = r'(?:\\{CHAR})'
domainliteral = r'(?:\[(?:{dtext|quotedpair}*)\])'
dtext = r'[^\[\]\\\x0d]'
CHAR = r'[\x00-\x7f]'
specials = r'[\(\)<>@,;:\\"\.\[\]]"]'
SPACE = r'[ ]'
CTL = r'[\x00-\x1f\x7f]'
