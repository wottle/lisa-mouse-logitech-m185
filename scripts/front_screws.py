#!/usr/bin/env python3
"""v2 case: case screws at the front corners, hook tabs at the rear, parallel side walls, and logo
recesses deep enough to take a separately printed logo plate.

Builds from the v1 parts in models/v1:
  models/fdm/    top_shell.stl, top_shell_lisa_logo.stl  with parallel side walls, to print on a side
  models/resin/  top_shell.stl, top_shell_lisa_logo.stl  with v1's leaning side walls (like the original Lisa mouse)
  models/common/ base.stl and the Lisa logo plates
Usage: python3 scripts/front_screws.py
Requires: numpy, trimesh, rtree, manifold3d.
"""
import os, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from adjustable_buttons import *
# Everything is done in the top shell's frame S (inside of the shell = +z; the base sits at z = SEAT).
SEAT=33.2                       # ledge the base rests on
SCREW=[(-23.3,44.3),(23.3,44.3)]  # new case screws (S frame; base x is mirrored)
BOSS_R=3.3; BOSS_END=24.0       # shell boss radius and how far it runs toward the roof
OLD_SCREW_B=[(-23.89,-29.8),(23.89,-29.8)]   # v1 screw holes, base frame
LOGO_SHIFT=[26.81,-11.34,26.5]  # top_shell_lisa_logo.stl is the same shell, translated
# rear hooks: (x0,x1) of each base upright after widening, and of the shell tab that passes through it (S frame)
UPRIGHT=[(0.7,9.3),(-9.3,-3.9)]
TAB=[(3.0,7.0),(-7.8,-5.4)]
TAB_Z=(29.6,30.8)               # shell tab (1.2 thick)
SLOT_Z=(29.45,31.45)            # slot in the upright: 0.15 mm on the load side, room on the other for hooking in
OLD_PILOT=[(-24.2,-29.8),(24.2,-29.8)]       # v1 screw pilot holes in the shell's rear corner blocks (S frame)
# logo recesses. The top panel is a plane z = ROOF_A*y + ROOF_C (outside = -z); recesses are cut square to it.
ROOF_A,ROOF_C=-0.06934,7.43803
LOGO_T=1.4; LOGO_CLEAR=0.1; LOGO_BEVEL=0.4   # same plate thickness, clearance and back bevel as the Macintosh mouse
APPLE_C=(15.85,-20.78)                       # centre of the v1 Apple recess (9.0 x 9.4, 0.6 deep); the new one takes the Mac mouse's plate
LISA_BOX=(-0.8,20.8,-25.75,-15.8); LISA_R=1.2   # new Lisa recess (v1: 21.2 x 9.6, 1.0 deep, raised wordmark)
LISA_RELIEF=0.4                              # height of the wordmark on the Lisa plate
# PCB front hold-down, as on the Macintosh mouse: a standoff in the board's scroll-wheel cutout whose screw head clamps
# the 2 mm strip of board in front of the cutout, so the front of the board cannot lift when the rear screw is tightened.
PCB_SEAT=8.05                   # base frame: height of the two angled ledges the front of the board rests on
PCB_TOP=PCB_SEAT+1.6
ST_B=(-3.0,45.18)               # screw axis, base frame (same place on the board as on the Macintosh mouse)
PCB_FRONT=49.3                  # front edge of the board, base frame
# The shell's front wall leans in toward the roof and v1 left the board's front edge touching it. Relief pocket:
RELIEF_X=(-15.5,18.0)           # S frame (the board's front edge spans about -10.5..13.5)
RELIEF_Z=(25.0,SEAT+0.1)        # from 5.6 mm above the board down to the seat
RELIEF_WALL=1.3                 # front wall left behind the pocket (v1: 2.55)
FRONT_OUT=(49.30,0.2113,20.0)   # outside of the front wall: y = 49.30 + 0.2113*(z-20)
VARIANTS=(('fdm',True),('resin',False))   # (folder, parallel sides): FDM shells get vertical, flat, parallel side walls so they
                                           # print standing on a side; resin shells keep v1's leaning walls, as on the original
def outer_x(shell_tm,sgn,z,y=10.0):
    loc,_,_=shell_tm.ray.intersects_location(np.array([[sgn*80,y,z]],float),np.array([[-sgn,0,0]],float),multiple_hits=False)
    return float(loc[0][0])
def straighten_sides(shell_tm,x_in=23.0,x_full=26.5):
    """v1 side walls lean in toward the roof (about 2 mm per side). Move everything outboard of the raised top panel
    so the outside of each wall is vertical at the rim width. The top gets wider; the rim and the middle do not move."""
    m=shell_tm.copy(); v=m.vertices.copy(); zr=v[:,2].max()
    for sgn in (1,-1):
        k=(outer_x(shell_tm,sgn,33.0)-outer_x(shell_tm,sgn,13.0))/20.0*sgn       # lean per mm of height
        side=np.sign(v[:,0])==sgn
        w=np.clip((np.abs(v[:,0])-x_in)/(x_full-x_in),0,1); w=w*w*(3-2*w)
        v[side,0]+=sgn*(w*k*(zr-v[:,2]))[side]
    m.vertices=v; return m
def to_S(Mb):  return Mb.transform(np.asarray(aff([[-1,0,0],[0,1,0],[0,0,-1]],[0,0,Z_BASE])[:3,:]))
to_B=to_S                       # the same flip maps back
def wall_x(shell_tm,sgn,y,z):
    loc,_,_=shell_tm.ray.intersects_location(np.array([[0,y,z]],float),np.array([[sgn,0,0]],float),multiple_hits=True)
    return float(np.min(np.abs(loc[:,0])))
def shell_changes(shell_tm):
    """Returns (add, cut) solids in S that turn a v1 shell into the new one."""
    shell=to_man(shell_tm); hull=shell.hull()
    add=[]; cut=[]
    for sgn in (1,-1):
        # --- the v1 rear screw blocks stay (solid corners need less support when printing on a side); only their pilot holes are filled
        px,py=[p for p in OLD_PILOT if np.sign(p[0])==sgn][0]
        add.append(cyl(px,py,SEAT-14.0,SEAT,1.8)^hull)
        cut.append(box(0,0.01,0,0.01,0,0.01).translate([0,0,-50]))      # (nothing to cut here any more)
        # --- new front boss, webbed into the side and front walls, with a 45 degree ramp so it prints roof-down
        x,y=[s for s in SCREW if np.sign(s[0])==sgn][0]
        W=wall_x(shell_tm,sgn,y,BOSS_END)
        def foot(z0,z1): return cyl(x,y,z0,z1,BOSS_R)+box(min(x,sgn*31),max(x,sgn*31),y-2.6,y+2.6,z0,z1)+box(x-2.6,x+2.6,y,53,z0,z1)
        ramp=foot(BOSS_END-9.0,BOSS_END).trim_by_plane([-sgn,0,1],(BOSS_END-W)/2**0.5)
        add.append((foot(BOSS_END,SEAT)+ramp)^hull)
        cut.append(cyl(x,y,SEAT-8.0,SEAT+1,1.35))
    for (x0,x1) in TAB:                                   # rear tabs that hook through the base uprights
        gus=box(x0,x1,-37.0,-34.3,TAB_Z[0]-2.0,TAB_Z[0]).trim_by_plane([0,-1,1],(34.3+TAB_Z[0])/2**0.5)   # 45 degree gusset so the tab prints roof-down
        add.append((box(x0,x1,-37.0,-32.35,TAB_Z[0],TAB_Z[1])+gus)^hull)
    return add,cut
def roof_frame(M,cx,cy,inv=False):
    """local frame on the top panel: origin at (cx,cy) on the surface, z = into the shell, square to the panel."""
    th=np.degrees(np.arctan(ROOF_A)); p=[cx,cy,ROOF_A*cy+ROOF_C]
    return M.translate([-p[0],-p[1],-p[2]]).rotate([-th,0,0]) if inv else M.rotate([th,0,0]).translate(p)
def rrect(w,h,r): return mf.CrossSection.square([w-2*r,h-2*r],True).offset(r,mf.JoinType.Round,circular_segments=48)
def apple_outline():
    """outline of the Macintosh mouse's logo plate (apple_logo_plate_blank.stl), so the same plate fits here"""
    return to_man(tm('apple_logo_plate_blank')).project().offset(LOGO_CLEAR,mf.JoinType.Round)
def lisa_outline(): x0,x1,y0,y1=LISA_BOX; return rrect(x1-x0,y1-y0,LISA_R)
def lisa_centre(): x0,x1,y0,y1=LISA_BOX; return (x0+x1)/2,(y0+y1)/2
def logo_recess(S,outline,c):
    return S-roof_frame(outline.extrude(6.0).translate([0,0,LOGO_T-6.0]),*c)
def plate(outline,relief=None):
    """Plate for a recess, on the bed: z=0 is the back (bevelled), the top is the show face."""
    o=outline.offset(-LOGO_CLEAR,mf.JoinType.Round)
    back=(o.offset(-LOGO_BEVEL,mf.JoinType.Round).extrude(0.01)+o.extrude(0.01).translate([0,0,LOGO_BEVEL])).hull()
    t=LOGO_T-(LISA_RELIEF if relief is not None else 0)
    P=back+o.extrude(t-LOGO_BEVEL).translate([0,0,LOGO_BEVEL])
    if relief is not None: P=P+(relief^o.offset(-0.6,mf.JoinType.Round)).extrude(LISA_RELIEF).translate([0,0,t])
    return P
def lisa_wordmark(v1_logo_shell):
    """the raised 'Lisa' wordmark of the v1 shell as a 2D outline in plate coordinates (seen from outside)"""
    L=roof_frame(v1_logo_shell,*lisa_centre(),inv=True)^box(-10.2,10.2,-4.3,4.3,0.35,0.75)
    return L.rotate([180,0,0]).project().simplify(0.01).rotate(180)      # turned so it reads upright in the plate file
def new_shell(shell_tm,logo=None,parallel=True):
    """logo: None = leave the top alone, False = Apple recess only, True = Lisa recess. parallel: straighten the side walls (FDM)"""
    if parallel: shell_tm=straighten_sides(shell_tm)
    add,cut=shell_changes(shell_tm); S=to_man(shell_tm)
    # order: remove old bosses, add new features, then drill
    S=S-cut[0]-cut[2]
    for a in add: S=S+a
    S=S-cut[1]-cut[3]
    y0,k,zr=FRONT_OUT; n=np.array([0,-1.0,k])                 # relief for the front edge of the PCB
    S=S-box(RELIEF_X[0],RELIEF_X[1],40,60,RELIEF_Z[0],RELIEF_Z[1]).trim_by_plane(list(n/np.linalg.norm(n)),(-(y0-k*zr-RELIEF_WALL))/np.linalg.norm(n))
    if logo is True: S=logo_recess(S,lisa_outline(),lisa_centre())
    if logo is False: S=logo_recess(S,apple_outline(),APPLE_C)
    S=max(S.decompose(),key=lambda d:d.volume()).simplify(0.003)
    return max(S.decompose(),key=lambda d:d.volume())
def new_base():
    B=to_man(tm('base'))                                   # base frame
    for x,y in OLD_SCREW_B: B=B+cyl(x,y,1.4,7.08,3.3)      # plug the old screw holes
    for (x,y) in SCREW:
        xb=-x
        B=B+cyl(xb,y,1.4,7.08,3.4)
    for (x,y) in SCREW:
        xb=-x
        B=B-cyl(xb,y,0,8,1.65)-cyl(xb,y,0,2.9,3.15)-cyl(xb,y,2.899,4.4,3.15,1.65)     # clearance, recess, countersink
    x,y=ST_B                                               # PCB front standoff, tied into the front wall
    B=B+box(x-3.5,x+3.5,y-3.0,48.6,1.5,PCB_SEAT)-cyl(x,y,2.6,PCB_SEAT+1,1.35)
    Bs=to_S(B)
    for (u0,u1),(t0,t1) in zip(UPRIGHT,TAB):
        Bs=Bs+box(u0,u1,-34.2,-32.75,26.0,36.2)            # widen the upright
        Bs=Bs-box(t0-0.4,t1+0.4,-36,-32.0,SLOT_Z[0],SLOT_Z[1])
    return max(to_B(Bs).decompose(),key=lambda d:d.volume()).simplify(0.0005)
def build_case(parallel=True):
    st=tm('top_shell'); sl=tm('top_shell_lisa_logo')
    shell=new_shell(st,logo=False,parallel=parallel)
    sl_S=sl.copy(); sl_S.apply_translation([-v for v in LOGO_SHIFT])
    logo=new_shell(sl_S,logo=True,parallel=parallel).translate(LOGO_SHIFT)
    word=lisa_wordmark(to_man(sl_S))
    return shell,logo,new_base(),plate(lisa_outline(),word),plate(lisa_outline())
def save(M,sub,n):
    d=os.path.join(MODELS,sub); os.makedirs(d,exist_ok=True)
    t=to_tm(M); t.export(os.path.join(d,n+'.stl')); t2=trimesh.load(os.path.join(d,n+'.stl'))
    print(f'{sub+"/"+n:28s} tris {len(t2.faces):6d} watertight {t2.is_watertight} bodies {len(M.decompose())} size {t2.extents.round(1)}')
def check_case(shell,base,R,Lb,St):
    P={'shell':shell,'base':to_S(base),'right':R,'left':Lb,'retainer':St}; ks=list(P); bad=0
    for i in range(len(ks)):
        for j in range(i+1,len(ks)):
            v=(P[ks[i]]^P[ks[j]]).volume(); g=P[ks[i]].min_gap(P[ks[j]],1.5) if v<1e-6 else 0
            if {ks[i],ks[j]}=={'shell','base'}:      # the two meet on the seat plane; only count overlap away from it
                v=((P[ks[i]]^P[ks[j]])-box(-40,40,-45,60,SEAT-0.15,SEAT+0.15)).volume()
            print(f'  {ks[i]:9s} x {ks[j]:9s} overlap {v:6.3f} mm3  gap {g:.2f}'); bad+=v>0.6
    def rot(M,deg): return M.translate([0,-SEAT_Y,-pin_z]).rotate([deg,0,0]).translate([0,SEAT_Y,pin_z])
    for deg in (1.5,3.0):
        for k in ('right','left'):
            for o in ('shell','base','retainer'):
                v=(rot(P[k],deg)^P[o]).volume()
                if v>0.6: print(f'  pressed {deg}: {k} x {o} overlap {v:.2f}'); bad+=1
    return bad

if __name__=='__main__':
    shells={}
    for sub,par in VARIANTS:
        shell,logo,base,lplate,lblank=build_case(par); shells[sub]=shell
        save(shell,sub,'top_shell'); save(logo,sub,'top_shell_lisa_logo')
    for n,M in (('base',base),('lisa_logo_plate',lplate),('lisa_logo_plate_blank',lblank)): save(M,'common',n)
    _,R,Lb,St=build()                                      # v2 buttons and retainer
    bad=0
    for sub,shell in shells.items(): print(f'=== {sub} shell'); bad+=check_case(shell,base,R,Lb,St)
    print('problems:',bad)
