import math,re
def oklch_to_lin(L,C,h):
    a=C*math.cos(math.radians(h)); b=C*math.sin(math.radians(h))
    l_=L+0.3963377774*a+0.2158037573*b; m_=L-0.1055613458*a-0.0638541728*b; s_=L-0.0894841775*a-1.2914855480*b
    l,m,s=l_**3,m_**3,s_**3
    r=4.0767416621*l-3.3077115913*m+0.2309699292*s; g=-1.2684380046*l+2.6097574011*m-0.3413193965*s; bb=-0.0041960863*l-0.7034186147*m+1.7076147010*s
    return [min(max(x,0),1) for x in (r,g,bb)]
def lum(c): r,g,b=oklch_to_lin(*c); return 0.2126*r+0.7152*g+0.0722*b
def ratio(a,b): la,lb=lum(a),lum(b); hi,lo=max(la,lb),min(la,lb); return (hi+0.05)/(lo+0.05)
css=open("src/styles/tokens.css",encoding="utf-8").read()
def block(sel):
    i=css.index(sel); j=css.index("}",i); return dict((k,tuple(map(float,v.split()[:3]))) for k,v in re.findall(r"--([\w-]+):\s*oklch\(([^)/]+)",css[i:j]))
light=block(":root {"); dark={**light,**block(':root[data-theme="dark"]')}
pairs=[("ink-3","bg"),("ink-3","surface"),("ink-3","surface-2"),("ink-3","surface-3"),("ink-2","surface-2"),("accent","bg"),("accent","surface"),("accent-ink","accent"),("accent-soft-ink","accent-soft"),("warn-ink","warn-soft"),("danger-ink","danger-soft"),("ink-2","bg")]
for name,t in (("light",light),("dark",dark)):
    print(name, ", ".join(f"{a}/{b}={ratio(t[a],t[b]):.2f}" for a,b in pairs))
