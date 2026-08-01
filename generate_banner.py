#!/usr/bin/env python3
"""
yuva-1237 GitHub Profile Banner Generator
Outputs dark.svg + light.svg  (~900KB each)

Usage:  python generate_banner.py photo.jpg
Needs:  pip install Pillow numpy scipy   (all already installed)
"""
import sys, math, random
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from scipy import ndimage

random.seed(42); np.random.seed(42)

# ── canvas ────────────────────────────────────────────────────────────────────
W, H, TITLE_H = 1180, 610, 36

# ── portrait grid & SVG position ──────────────────────────────────────────────
GW, GH  = 300, 340                          # dither grid cols × rows
PX, PY  = 28, TITLE_H + 8                   # SVG origin
PW, PH  = 350, H - TITLE_H - 16             # portrait SVG size
SX, SY  = PW / GW, PH / GH                 # px per grid cell
DR      = 0.70 * min(SX, SY)               # dot radius

# ── info panel ────────────────────────────────────────────────────────────────
IX, IY  = PX + PW + 14, TITLE_H + 8
IW, IH  = W - IX - 12, H - TITLE_H - 16

# ── palette ───────────────────────────────────────────────────────────────────
C = dict(
    bg="#0A101F", chrome="#111827", panel="#0D1520", border="#1E293B",
    dot_dk="#A78BFA", dot_lt="#7C3AED",
    cyan="#22D3EE", cyan2="#0891B2", green="#10B981",
    live="#EF4444", hi="#F8FAFC", mid="#94A3B8", lo="#64748B", pill="#1E293B",
    bg_lt="#F1F5F9", chrome_lt="#E2E8F0", border_lt="#CBD5E1", panel_lt="#FFFFFF",
)

# ── profile data ──────────────────────────────────────────────────────────────
ROWS = [
    ("Subject",        "YUVA THILAGAN"),
    ("Role",           "AI Engineer"),
    ("Origin",         "Chennai, India"),
    ("Education",      "CS Engineering"),
    ("Status",         "Building + Learning + Shipping"),
    ("ToolChain",      "VS Code · Git · Figma"),
    ("Core.Lang",      "Python · JS · SQL · Java"),
    ("Core.Frontend",  "React · TS · Vite"),
    ("Core.Backend",   "FastAPI · REST APIs"),
    ("Core.Database",  "MongoDB · PostgreSQL"),
    ("Core.Infra",     "AWS · Docker · GH Actions"),
    ("Grid.Mail",      "yuvathilagan@gmail.com"),
    ("Grid.Portfolio", "yuvathilagan.vercel.app"),
    ("Grid.LinkedIn",  "linkedin/yuvathilagan"),
    ("Grid.GitHub",    "yuva-1237"),
    ("Grid.Instagram", "@_y_u_v_a_10_"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# IMAGE PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════

def load_photo(path):
    img = Image.open(path).convert("RGB")
    iw, ih = img.size
    ratio = GW / GH
    if iw / ih > ratio:
        nw = int(ih * ratio); img = img.crop(((iw-nw)//2, 0, (iw-nw)//2+nw, ih))
    else:
        nh = int(iw / ratio); img = img.crop((0, 0, iw, nh))   # top crop = head+shoulders
    img = img.resize((GW, GH), Image.LANCZOS)
    img = ImageOps.autocontrast(img, cutoff=1)
    img = img.filter(ImageFilter.UnsharpMask(radius=3, percent=140, threshold=0))
    img = ImageEnhance.Contrast(img).enhance(1.3)
    return img

def floyd_steinberg(gray):
    """Serpentine 1-bit FS dither. 1 = dark dot present."""
    h, w = gray.shape; buf = gray / 255.0
    out = np.zeros((h, w), np.uint8)
    for y in range(h):
        ltr = y % 2 == 0; xs = range(w) if ltr else range(w-1,-1,-1); s = 1 if ltr else -1
        for x in xs:
            v = buf[y,x]; q = 1.0 if v >= 0.5 else 0.0
            out[y,x] = 1 - int(q); e = v - q
            def p(ry,rx,w_):
                if 0<=ry<h and 0<=rx<w: buf[ry,rx] = np.clip(buf[ry,rx]+e*w_,0,1)
            p(y,x+s,7/16); p(y+1,x-s,3/16); p(y+1,x,5/16); p(y+1,x+s,1/16)
    return out

def segment_fg(rgb):
    """Foreground mask via background-colour distance + morphology."""
    f = np.array(rgb, np.float64); h,w = f.shape[:2]; m=25
    bg = np.median(np.vstack([f[:m,:m].reshape(-1,3),f[:m,-m:].reshape(-1,3),
                               f[-m:,:m].reshape(-1,3),f[-m:,-m:].reshape(-1,3),
                               f[:m,w//3:2*w//3].reshape(-1,3)]),axis=0)
    dist = np.sqrt(np.sum((f-bg)**2,axis=2))
    mask = dist > np.percentile(dist,28)
    mask = ndimage.binary_closing(mask,structure=np.ones((9,9)),iterations=3)
    mask = ndimage.binary_fill_holes(mask)
    lbl,nf = ndimage.label(mask)
    if nf: mask = lbl==(np.argmax([np.sum(lbl==i) for i in range(1,nf+1)])+1)
    return ndimage.binary_dilation(mask,iterations=4).astype(bool)

def get_dots(d, mask=None):
    m = d==1
    if mask is not None: m &= mask
    r,c = np.where(m)
    return np.column_stack([c.astype(np.float32),r.astype(np.float32)])

def to_svg(g):
    return np.column_stack([PX+(g[:,0]+0.5)*SX, PY+(g[:,1]+0.5)*SY])

# ═══════════════════════════════════════════════════════════════════════════════
# LOGO DOT CLOUDS  (Python · React · AI/neural-net)
# ═══════════════════════════════════════════════════════════════════════════════

def logo_python(n,cx,cy,r):
    pts=[]
    for i in range(n//2):
        t=i/(n//2)*2*math.pi
        pts.append([cx+r*.38*math.cos(t)+r*.10*math.cos(2*t)+random.gauss(0,r*.04),
                    cy+r*(-.44+.88*i/(n//2))+r*.08*math.sin(t)+random.gauss(0,r*.04)])
    for i in range(n-n//2):
        t=i/(n-n//2)*2*math.pi
        pts.append([cx-r*.38*math.cos(t)-r*.10*math.cos(2*t)+random.gauss(0,r*.04),
                    cy+r*(.44-.88*i/(n-n//2))+r*.08*math.sin(t)+random.gauss(0,r*.04)])
    return np.array(pts,np.float32)

def logo_react(n,cx,cy,r):
    pts=[]; per=n//3
    for orbit in range(3):
        a=orbit*math.pi/3; ca,sa=math.cos(a),math.sin(a)
        for i in range(per):
            t=i/per*2*math.pi; xl=r*.85*math.cos(t); yl=r*.28*math.sin(t)
            pts.append([cx+xl*ca-yl*sa+random.gauss(0,r*.03),
                        cy+xl*sa+yl*ca+random.gauss(0,r*.03)])
    while len(pts)<n:
        a=random.uniform(0,2*math.pi); rr=random.uniform(0,r*.1)
        pts.append([cx+rr*math.cos(a),cy+rr*math.sin(a)])
    return np.array(pts[:n],np.float32)

def logo_ai(n,cx,cy,r):
    pts=[]
    out6=[(cx+r*.65*math.cos(i*math.pi/3-math.pi/6),cy+r*.65*math.sin(i*math.pi/3-math.pi/6)) for i in range(6)]
    in6 =[(cx+r*.30*math.cos(i*math.pi/3),cy+r*.30*math.sin(i*math.pi/3)) for i in range(6)]
    nodes=out6+in6+[(cx,cy)]
    pn=n//(len(nodes)+12)
    for (nx,ny) in nodes:
        for _ in range(pn): pts.append([nx+random.gauss(0,r*.04),ny+random.gauss(0,r*.04)])
    edges=[(i,12) for i in range(6)]+[(i,i+6) for i in range(6)]+[(i,(i+1)%6+6) for i in range(6)]
    pe=(n-len(pts))//max(len(edges),1)
    for a,b in edges:
        ax,ay=nodes[a]; bx,by=nodes[b]
        for j in range(pe):
            t=j/max(pe-1,1)
            pts.append([ax+(bx-ax)*t+random.gauss(0,r*.02),ay+(by-ay)*t+random.gauss(0,r*.02)])
    while len(pts)<n:
        a=random.uniform(0,2*math.pi); rr=random.uniform(0,r*.65)
        pts.append([cx+rr*math.cos(a),cy+rr*math.sin(a)])
    return np.array(pts[:n],np.float32)

def greedy_ot(src,dst):
    n=min(len(src),len(dst)); s,d=src[:n],dst[:n]
    used=np.zeros(n,bool); order=np.zeros(n,int)
    for i in range(n):
        dists=np.sum((d-s[i])**2,axis=1); dists[used]=np.inf
        j=int(np.argmin(dists)); order[i]=j; used[j]=True
    return order

# ═══════════════════════════════════════════════════════════════════════════════
# SVG COMPONENT BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def f1(v): return f"{v:.1f}"
def f2(v): return f"{v:.2f}"
def f3(v): return f"{v:.3f}"

def title_bar(dark):
    bg=C["chrome"] if dark else C["chrome_lt"]
    txt=C["mid"] if dark else "#64748B"
    return (f'<rect x="0" y="0" width="{W}" height="{TITLE_H}" rx="8" fill="{bg}"/>'
            f'<rect x="0" y="{TITLE_H//2}" width="{W}" height="{TITLE_H//2}" fill="{bg}"/>'
            f'<circle cx="16" cy="18" r="5.5" fill="#FF5F57"/>'
            f'<circle cx="36" cy="18" r="5.5" fill="#FEBC2E"/>'
            f'<circle cx="56" cy="18" r="5.5" fill="#28C840"/>'
            f'<text x="{W//2}" y="23" text-anchor="middle" '
            f'font-family="JetBrains Mono,monospace" font-size="12" fill="{txt}">profile.sh --live</text>')

def live_badge():
    lx,ly = W-80,9
    return (f'<rect x="{lx}" y="{ly}" width="64" height="18" rx="9" fill="#7f1d1d">'
            f'<animate attributeName="opacity" values="1;0.4;1" dur="1.5s" repeatCount="indefinite"/>'
            f'</rect>'
            f'<circle cx="{lx+12}" cy="{ly+9}" r="3.5" fill="{C["live"]}">'
            f'<animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite"/>'
            f'</circle>'
            f'<text x="{lx+22}" y="{ly+13}" font-family="JetBrains Mono,monospace" '
            f'font-size="10" fill="{C["live"]}" font-weight="bold">LIVE</text>')

def portrait_frame(dark):
    bg=C["panel"] if dark else C["panel_lt"]
    bd=C["border"] if dark else C["border_lt"]
    lb=C["cyan"]   if dark else C["cyan2"]
    return (f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="4" fill="{bg}" stroke="{bd}" stroke-width="1"/>'
            f'<text x="{PX+PW//2}" y="{PY+18}" text-anchor="middle" '
            f'font-family="JetBrains Mono,monospace" font-size="10" fill="{lb}" letter-spacing="3">VISUAL.MAP</text>')

def info_panel(dark):
    hi  = C["hi"]     if dark else "#0F172A"
    mid = C["mid"]    if dark else "#475569"
    lo  = C["lo"]     if dark else "#94A3B8"
    cy  = C["cyan"]   if dark else C["cyan2"]
    bg  = C["panel"]  if dark else C["panel_lt"]
    bd  = C["border"] if dark else C["border_lt"]
    pb  = C["pill"]   if dark else "#E2E8F0"
    L=[]
    L.append(f'<rect x="{IX}" y="{IY}" width="{IW}" height="{IH}" rx="4" fill="{bg}" stroke="{bd}" stroke-width="1"/>')
    L.append(f'<text x="{IX+16}" y="{IY+22}" font-family="JetBrains Mono,monospace" font-size="11" font-weight="600" fill="{cy}" letter-spacing="3">SYSTEM.INFO</text>')
    L.append(f'<line x1="{IX+16}" y1="{IY+30}" x2="{IX+IW-16}" y2="{IY+30}" stroke="{bd}" stroke-width="1" stroke-dasharray="2,4"/>')
    # LIVE in panel
    bx,by=IX+IW-72,IY+10
    L.append(f'<rect x="{bx}" y="{by}" width="58" height="16" rx="8" fill="#7f1d1d">'
             f'<animate attributeName="opacity" values="1;0.4;1" dur="1.5s" repeatCount="indefinite"/>'
             f'</rect>'
             f'<circle cx="{bx+10}" cy="{by+8}" r="3" fill="{C["live"]}">'
             f'<animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite"/>'
             f'</circle>'
             f'<text x="{bx+20}" y="{by+12}" font-family="JetBrains Mono,monospace" font-size="10" fill="{C["live"]}" font-weight="bold">LIVE</text>')
    CW=7.5; VX=IX+IW-16; ry=IY+50; rh=int((IH-80)/len(ROWS))
    for k,v in ROWS:
        lx=IX+16
        vcol=hi if k=="Subject" else (cy if k.startswith("Grid.") else mid)
        L.append(f'<text x="{lx}" y="{ry}" font-family="JetBrains Mono,monospace" font-size="12" fill="{mid}">{k}</text>')
        dx=lx+(len(k)+0.6)*CW; de=VX-(len(v)+0.6)*CW
        if de>dx+8:
            nd=max(1,int((de-dx)/(CW*.95))); dots="·"*nd
            L.append(f'<text x="{dx:.1f}" y="{ry}" font-family="JetBrains Mono,monospace" font-size="12" fill="{lo}" textLength="{de-dx:.1f}" lengthAdjust="spacingAndGlyphs">{dots}</text>')
        L.append(f'<text x="{VX}" y="{ry}" text-anchor="end" font-family="JetBrains Mono,monospace" font-size="12" fill="{vcol}">{v}</text>')
        ry+=rh
        if k in ("Status","Core.Infra"):
            L.append(f'<line x1="{IX+16}" y1="{ry-4}" x2="{IX+IW-16}" y2="{ry-4}" stroke="{bd}" stroke-width="1" stroke-dasharray="2,4"/>')
    py_=IY+IH-30
    L.append(f'<rect x="{IX+16}" y="{py_}" width="152" height="22" rx="11" fill="{pb}"/>')
    L.append(f'<text x="{IX+92}" y="{py_+15}" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="12" fill="{cy}">◈  @yuva-1237</text>')
    return "\n".join(L)

# ═══════════════════════════════════════════════════════════════════════════════
# ANIMATION BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def intro_anim(svg_dots, color, n_groups=60):
    """60 spatially-scattered groups, staggered fade-in over 2 s."""
    def morton(x,y):
        z=0
        for i in range(12): z|=((int(x)>>i)&1)<<(2*i)|((int(y)>>i)&1)<<(2*i+1)
        return z
    gx=np.clip(((svg_dots[:,0]-PX)/SX).astype(int),0,GW-1)
    gy=np.clip(((svg_dots[:,1]-PY)/SY).astype(int),0,GH-1)
    order=np.argsort([morton(x,y) for x,y in zip(gx,gy)])
    groups=[[] for _ in range(n_groups)]
    for i,idx in enumerate(order): groups[i%n_groups].append(idx)
    parts=[]
    for g,idxs in enumerate(groups):
        if not idxs: continue
        begin=g/n_groups*2.0
        dots="".join(f'<circle cx="{f1(svg_dots[i,0])}" cy="{f1(svg_dots[i,1])}" r="{f2(DR)}" shape-rendering="crispEdges"/>' for i in idxs)
        parts.append(f'<g fill="{color}" opacity="0">{dots}<animate attributeName="opacity" values="0;1" dur="0.45s" begin="{f3(begin)}s" fill="freeze"/></g>')
    return "\n".join(parts)

def portrait_loop(svg_dots, logo_centroids, color, n_bands=94):
    """
    94 drift bands. T=14.2s loop.
    Portrait 2.2s → per logo: 0.9s drift + 2.2s hold + 0.9s return.
    """
    n=len(svg_dots); cx=np.mean(svg_dots[:,0]); cy=np.mean(svg_dots[:,1])
    d=np.sqrt((svg_dots[:,0]-cx)**2+(svg_dots[:,1]-cy)**2)+np.random.normal(0,4,n)
    order=np.argsort(d); bands=[[] for _ in range(n_bands)]
    for i,idx in enumerate(order): bands[i%n_bands].append(idx)
    Tp=2.2; Ttr=0.9; Th=2.2; Tcy=Ttr+Th+Ttr
    T=Tp+len(logo_centroids)*Tcy
    def t(s): return round(s/T,4)
    parts=[]
    for bi,idxs in enumerate(bands):
        if not idxs: continue
        bp=bi/n_bands
        dots="".join(f'<circle cx="{f1(svg_dots[i,0])}" cy="{f1(svg_dots[i,1])}" r="{f2(DR)}" shape-rendering="crispEdges"/>' for i in idxs)
        tv=["0,0","0,0"]; kt=[0,t(Tp)]; op=["1","1"]; ok=[0,t(Tp)]
        for li,(lcx,lcy) in enumerate(logo_centroids):
            dx=(lcx-cx)*0.42*(0.3+0.7*bp); dy=(lcy-cy)*0.42*(0.3+0.7*bp)
            t0=Tp+li*Tcy; t1=t0+Ttr; t2=t1+Th; t3=t2+Ttr
            tv.extend([f"{dx:.1f},{dy:.1f}",f"{dx:.1f},{dy:.1f}","0,0"])
            kt.extend([t(t1),t(t2),t(t3)])
            op.extend(["0.1","0.1","1"]); ok.extend([t(t0+Ttr*.5),t(t2+Ttr*.5),t(t3)])
        kt.append(1.0); tv.append("0,0"); ok.append(1.0); op.append("1")
        ns=len(kt)-1; sp=";".join(["0.4 0 0.6 1"]*ns)
        nos=len(ok)-1; spo=";".join(["0.4 0 0.6 1"]*nos)
        parts.append(
            f'<g fill="{color}">{dots}'
            f'<animateTransform attributeName="transform" type="translate" values="{";".join(tv)}" keyTimes="{";".join(str(k) for k in kt)}" dur="{T:.1f}s" repeatCount="indefinite" calcMode="spline" keySplines="{sp}"/>'
            f'<animate attributeName="opacity" values="{";".join(op)}" keyTimes="{";".join(str(k) for k in ok)}" dur="{T:.1f}s" repeatCount="indefinite" calcMode="spline" keySplines="{spo}"/>'
            f'</g>')
    return "\n".join(parts), T

def travellers(clouds, color, T, N=900):
    """900 dots morphing between 3 logos via greedy OT."""
    Tp=2.2; Ttr=0.9; Th=2.2; Tcy=Ttr+Th+Ttr
    resampled=[]
    for cloud in clouds:
        idx=(np.random.choice(len(cloud),N,replace=len(cloud)<N))
        resampled.append(cloud[idx])
    parts=[]
    for di in range(N):
        xs=[]; ys=[]; ops=[]; kt=[]
        def ap(t_,x_,y_,o_):
            kt.append(f"{t_:.4f}"); xs.append(f1(x_)); ys.append(f1(y_)); ops.append(str(o_))
        p0=resampled[0][di]
        ap(0,p0[0],p0[1],0); ap(round(Tp/T,4),p0[0],p0[1],0)
        for li in range(len(resampled)):
            t0=Tp+li*Tcy; t1=t0+Ttr; t2=t1+Th; t3=t0+Tcy
            cur=resampled[li][di]; nxt=resampled[(li+1)%len(resampled)][di]
            ap(round((t0+Ttr*.2)/T,4),cur[0],cur[1],1)
            ap(round(t1/T,4),cur[0],cur[1],1)
            ap(round(t2/T,4),cur[0],cur[1],1)
            ap(round((t2+Ttr*.8)/T,4),nxt[0],nxt[1],0 if li==len(resampled)-1 else 1)
            ap(round(t3/T,4),nxt[0],nxt[1],0 if li==len(resampled)-1 else 1)
        ap(1.0,p0[0],p0[1],0)
        ns=len(kt)-1; sp=";".join(["0.4 0 0.6 1"]*ns); kt_s=";".join(kt)
        parts.append(
            f'<circle r="{f2(DR*1.12)}" fill="{color}" shape-rendering="crispEdges">'
            f'<animate attributeName="cx" values="{";".join(xs)}" keyTimes="{kt_s}" dur="{T:.1f}s" repeatCount="indefinite" calcMode="spline" keySplines="{sp}"/>'
            f'<animate attributeName="cy" values="{";".join(ys)}" keyTimes="{kt_s}" dur="{T:.1f}s" repeatCount="indefinite" calcMode="spline" keySplines="{sp}"/>'
            f'<animate attributeName="opacity" values="{";".join(ops)}" keyTimes="{kt_s}" dur="{T:.1f}s" repeatCount="indefinite"/>'
            f'</circle>')
    return "\n".join(parts)

# ═══════════════════════════════════════════════════════════════════════════════
# MASTER SVG BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

def build_svg(intro, loop, trav, dark, T):
    bg=C["bg"] if dark else C["bg_lt"]
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<rect width="{W}" height="{H}" fill="{bg}" rx="8"/>
{title_bar(dark)}
{live_badge()}
{portrait_frame(dark)}
<!-- Intro layer: plays once (0-2s), 60 scattered groups -->
<g id="intro">{intro}</g>
<!-- Loop layer: portrait dissolution + logo drift (fades in at 1.8s) -->
<g id="loop" opacity="0">
<animate attributeName="opacity" values="0;0;1" keyTimes="0;0.88;1" dur="2.2s" fill="freeze"/>
{loop}
</g>
<!-- Traveller layer: 900-dot logo morphing -->
<g id="travellers">{trav}</g>
{info_panel(dark)}
</svg>'''

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    photo = sys.argv[1] if len(sys.argv)>1 else "photo.jpg"
    if not Path(photo).exists():
        print(f"ERROR: {photo} not found. Save your photo as photo.jpg in this folder.")
        sys.exit(1)

    print(f"[1/7] Loading and enhancing {photo}...")
    img = load_photo(photo)
    rgb = np.array(img)

    print("[2/7] Floyd-Steinberg dithering (serpentine)...")
    gray = np.array(img.convert("L"), np.float64)
    dit  = floyd_steinberg(gray)

    print("[3/7] Segmenting foreground for dark mode...")
    fg   = ndimage.binary_erosion(segment_fg(rgb), iterations=1)

    print("[4/7] Building dot arrays...")
    dots_dk = get_dots(dit, fg)        # dark mode: subject only
    dots_lt = get_dots(dit)            # light mode: all dots
    svg_dk  = to_svg(dots_dk)
    svg_lt  = to_svg(dots_lt)
    print(f"    dark={len(dots_dk):,}  light={len(dots_lt):,} dots")

    print("[5/7] Building logo clouds (Python · React · AI)...")
    lcx, lcy, lr = PX+PW//2, PY+PH//2, min(PW,PH)*0.26
    l0 = logo_python(900, lcx, lcy, lr)
    l1 = logo_react (900, lcx, lcy, lr)
    l2 = logo_ai    (900, lcx, lcy, lr)
    centroids = [(lcx,lcy),(lcx,lcy),(lcx,lcy)]   # all logos centred on portrait

    print("[6/7] Building animations (intro + loop + travellers)...")
    col_dk, col_lt = C["dot_dk"], C["dot_lt"]

    intro_dk = intro_anim(svg_dk, col_dk)
    intro_lt = intro_anim(svg_lt, col_lt)

    loop_dk, T = portrait_loop(svg_dk, centroids, col_dk)
    loop_lt, _ = portrait_loop(svg_lt, centroids, col_lt)

    trav_dk = travellers([l0,l1,l2], col_dk, T)
    trav_lt = travellers([l0,l1,l2], col_lt, T)

    print("[7/7] Writing SVGs...")
    dk = build_svg(intro_dk, loop_dk, trav_dk, dark=True,  T=T)
    lt = build_svg(intro_lt, loop_lt, trav_lt, dark=False, T=T)

    Path("dark.svg").write_text(dk, encoding="utf-8")
    Path("light.svg").write_text(lt, encoding="utf-8")

    dkb = Path("dark.svg").stat().st_size//1024
    ltb = Path("light.svg").stat().st_size//1024
    print(f"\n✓  dark.svg  ({dkb} KB)")
    print(f"✓  light.svg ({ltb} KB)")
    print(f"\nLoop duration: {T:.1f}s  |  Dots: dark={len(dots_dk):,} light={len(dots_lt):,}")
    print("\nOpen dark.svg / light.svg in Chrome to verify, then:")
    print("  git add dark.svg light.svg && git push origin main")

if __name__ == "__main__":
    main()
