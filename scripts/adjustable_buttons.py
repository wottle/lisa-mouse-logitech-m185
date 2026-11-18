#!/usr/bin/env python3
"""Build the v2 buttons and retainer from the v1 parts in models/v1: screw-adjustable strikers, a hinge held without
play by two spring fingers on the retainer, and button caps that stand 1 mm higher.

Usage: python3 scripts/adjustable_buttons.py        (writes models/left_button.stl, right_button.stl, button_stop.stl)
Requires: numpy, trimesh, manifold3d.

All work is done with the parts assembled in the top shell's frame S (inside of the shell = +z), then each part is
written back in the frame its original STL used."""
import numpy as np, trimesh, manifold3d as mf, os
from manifold3d import Manifold, Mesh, CrossSection
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS=os.path.join(ROOT,'models'); V1=os.path.join(MODELS,'v1')
def tm(name):
    """v1 buttons and retainer come from models/v1; shell and base from models/."""
    p=os.path.join(V1,name+'.stl')
    if not os.path.exists(p): p=os.path.join(MODELS,name+'.stl')
    m=trimesh.load(p,force='mesh'); m.merge_vertices(digits_vertex=4); return m
def to_man(m):
    M=Manifold(Mesh(vert_properties=np.asarray(m.vertices,dtype=np.float32),tri_verts=np.asarray(m.faces,dtype=np.uint32))); assert M.status()==mf.Error.NoError,M.status(); return M
def to_tm(M):
    me=M.to_mesh(); return trimesh.Trimesh(np.asarray(me.vert_properties)[:,:3],np.asarray(me.tri_verts),process=False)
def box(x0,x1,y0,y1,z0,z1): return Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])
def cyl(x,y,z0,z1,r,r2=None,n=64): return Manifold.cylinder(z1-z0,r,r if r2 is None else r2,n).translate([x,y,z0])
def aff(R,t):
    M=np.eye(4); M[:3,:3]=R; M[:3,3]=t; return M

# ---- measured from the v1 parts -------------------------------------------------------------------------------
SEAT_Y,SEAT_FLOOR=17.188,10.391      # hinge pin seat in the shell
SLOPE=0.07                           # the shell's roof and inner ledge slope this much per mm in S
LEDGE_C=14.25                        # ledge plane: z = LEDGE_C - SLOPE*y
PIN_OLD_R=1.271; PIN_Z_R,PIN_Y_R=13.157,80.10   # right button's pin in its own file; left: up=x 3.587
BOSS=[(-11.60,10.35),(11.54,10.35)]  # retainer screw bosses (at the ledge surface)
Z_BASE=40.28                         # base frame z = Z_BASE - z_S ; base x = -x_S
# ---- design values ---------------------------------------------------------------------------------------------
PIN_R=1.43                           # fatter pin: 0.08 radial clearance in the r1.51 seat (was 0.24)
FINGER_GAP=0.25                      # the four rigid retainer fingers are only a backstop: this far above the pins with the plate screwed down hard
# Anti-sag: the switch pushes each button up at its outer front corner only, so the button's weight (and a finger
# pressing near the middle of the mouse) rolls it about the line hinge-outer-end -> striker, and the inner front
# corner drops by whatever play the pin has under the retainer. A thin spring finger per button, at the inner end of
# the pin, presses the pin onto its seat instead of leaving a gap there: no play, and nothing to adjust.
SPRING_X=(0.7,3.7)                   # spring finger, x range for the left button (mirrored for the right)
SPRING_T=1.0; SPRING_ROOT=10.4       # finger thickness; y where it leaves the plate (6.8 mm of free length, about 6 N/mm)
SPRING_PRELOAD=0.15                  # the finger's pad stands this far into the pin: about 1 N on each pin
FLANGE_TOP=10.95                     # roof-side face of the button flange (S frame); the left post starts here outboard of the cap
SIDE_CLEAR=0.35                      # side and front/back clearance from the shell for everything ahead of the hinge (y > HINGE_KEEP).
HINGE_KEEP=20.5                      # The flange has a step outboard of the rim round the underside of the window; v1 left it touching
                                     # that rim (left button 0 mm, right 0.15 mm), so the left button dragged and stuck down.
LIFT_FREE=1.5                        # degrees the button may lift from its design rest before anything but the front edge of the flange
STOP_Y=41.5                          # touches the shell (the right button's natural stop is at 1.2 deg; v1 left hit the window rim at 0.5)
CAP_RAISE=1.0                        # button caps stand this much higher above the shell than v1 (v1: 1.6 mm)
SW_L=(19.92,34.5); SW_R=(-16.73,34.5)   # switch plungers in S (9 / 12 mm from the base edges)
SW_TOP_B=17.5                        # plunger free height in the base frame
COL_R=3.0; COL_Y=34.0; COL_BOT=Z_BASE-(SW_TOP_B+2.8)   # striker post; an M3x8 countersunk screw, head down, sets the height
PLATE_T=2.6
pin_z=SEAT_FLOOR+PIN_R
A_R=aff([[-1,0,0],[0,1,0],[0,0,-1]],[14.25,SEAT_Y-PIN_Y_R,pin_z+PIN_Z_R])          # right button file -> S
A_L=aff([[0,0,1],[0,1,0],[-1,0,0]],[0.35,SEAT_Y-PIN_Y_R,pin_z+3.587])               # left button file -> S
def xf(M,A): return M.transform(np.asarray(A[:3,:],dtype=np.float64))
def inv(A): return np.linalg.inv(A)
def xcyl(x0,x1,y,z,r): return Manifold.cylinder(x1-x0,r,r,64).rotate([0,90,0]).translate([x0,y,z])
def new_button(B,side,shell):
    bb=B.bounding_box(); x0,x1=bb[0],bb[3]
    sx,sy=(SW_R if side=='R' else SW_L)
    # hinge pin: same axis height above the seat floor, fatter
    B=B+(xcyl(x0,x1,SEAT_Y,pin_z,PIN_R))
    # old fixed plunger blade: remove everything of it that hangs near the switch
    bx0,bx1=sx-6.8,sx+6.8
    B=B-box(bx0,bx1,33.6,37.2,12.9,40)
    # striker post
    col=cyl(sx,COL_Y,5.5,COL_BOT,COL_R)^box(-60,60,-60,36.55,0,60)
    roof=Manifold.batch_boolean([shell.translate([dx,0,dz]) for dx in (-0.3,0,0.3) for dz in (0,0.2,0.4)],mf.OpType.Add)   # keep 0.3-0.4 mm off the shell
    web=box(sx-COL_R,sx+COL_R,COL_Y-COL_R,36.55,5.5,14.6)                 # ties the post into the cap edge / flange
    add=(col+web)-roof
    # nothing new may stand in the gap between the cap's side wall and the window edge: there the left button's
    # post (its switch sits under the window edge) rubbed on the opening. Outboard of the cap wall the post stays
    # below the flange, so both buttons have the same outside.
    wb=(B^box(-60,60,29.0,33.0,6.5,9.0)).bounding_box(); s_=1 if side=='L' else -1
    xo=(wb[3] if s_>0 else wb[0])-s_*1.0        # 1 mm inside the wall's outer face: new material only joins the wall from inside
    add=add-box(min(xo,s_*60),max(xo,s_*60),-60,60,-10,FLANGE_TOP)
    B=B+add
    B=B-cyl(sx,COL_Y,COL_BOT-8.0,COL_BOT+1,1.35)
    # bare pin at the inner end for the retainer's spring finger
    s=1 if side=='L' else -1; w0,w1=sorted((s*0.0,s*(SPRING_X[1]+0.5)))
    B=B-(box(w0,w1,15.4,18.9,pin_z+PIN_R-0.3,30)-xcyl(w0-1,w1+1,SEAT_Y,pin_z,PIN_R))
    # taller cap: the part that shows through the window, copied CAP_RAISE further out
    B=B+(B^box(-30,30,25.0,39.0,-10,9.0)).translate([0,0,-CAP_RAISE])
    # free running: keep SIDE_CLEAR from the shell sideways and front-to-back ahead of the hinge. Only x/y offsets, so the
    # up-stop (flange front against the underside of the roof) is not touched.
    c=SIDE_CLEAR; d=c/np.sqrt(2)
    sh=[shell.translate([dx,dy,0]) for dx,dy in ((c,0),(-c,0),(0,c),(0,-c),(d,d),(d,-d),(-d,d),(-d,-d))]
    wide=Manifold.batch_boolean(sh+[shell],mf.OpType.Add)
    B=B-(wide^box(-60,60,HINGE_KEEP,60,-10,30))
    # ...and the same clearance for the full lift (the rim's outer face flares, so a lifted button meets it), so only the
    # front edge of the flange (y > STOP_Y) is the up-stop
    hinge=lambda M,deg: M.translate([0,-SEAT_Y,-pin_z]).rotate([deg,0,0]).translate([0,SEAT_Y,pin_z])
    lift=[hinge(wide,a) for a in np.linspace(0.25,LIFT_FREE+0.2,7)]
    B=B-(Manifold.batch_boolean(lift,mf.OpType.Add)^box(-60,60,HINGE_KEEP,STOP_Y,-10,30))
    return max(B.decompose(),key=lambda d:d.volume())
def new_stop(shell,old_stop_tm):
    o=to_man(old_stop_tm).project().translate([0,-0.3])
    slab=o.extrude(14).translate([0,0,7])
    n=np.array([0,SLOPE,1.0]); L=np.linalg.norm(n)
    S=slab.trim_by_plane(list(n),LEDGE_C/L)-shell                      # flat underside lying on the shell's ledge
    S=S-slab.trim_by_plane(list(n),(LEDGE_C+PLATE_T)/L)                # flat top, parallel to the ledge
    fz=(pin_z+PIN_R)+FINGER_GAP+SLOPE*(SEAT_Y+0.1)                     # finger underside plane constant
    S=S-(box(-40,40,15.25,40,0,30)-box(-40,40,15.25,40,0,30).trim_by_plane(list(n),fz/L))
    for x,y in BOSS:
        ax=lambda r0,r1,h: Manifold.cylinder(h,r0,r1,48).rotate([-np.degrees(np.arctan(SLOPE)),0,0])
        zl=LEDGE_C-SLOPE*y
        S=S-ax(1.65,1.65,6).translate([x,y+SLOPE*1,zl-1])
        S=S-ax(1.65,3.15,1.5).translate([x,y-SLOPE*(PLATE_T-1.5),zl+PLATE_T-1.5])     # countersink, head on the inside
    return max(S.decompose(),key=lambda d:d.volume())
def planes():
    n=np.array([0,SLOPE,1.0]); return n,np.linalg.norm(n)
def slab(c0,c1):
    """everything between two planes parallel to the ledge: c0 <= z + SLOPE*y <= c1"""
    n,L=planes(); big=box(-60,60,-60,60,-20,60)
    return big.trim_by_plane(list(n),c0/L)-big.trim_by_plane(list(n),c1/L)
def spring_fingers(S):
    """two thin fingers, flush with the plate's inner face, whose pads press the inner ends of the two pins onto their seats"""
    a,b=SPRING_X; top=LEDGE_C+PLATE_T
    S=S-box(-(b+0.7),b+0.7,SPRING_ROOT,24,0,30)                                   # slots round the fingers
    pad_c=(pin_z+PIN_R-SPRING_PRELOAD)+SLOPE*SEAT_Y                              # pad face: SPRING_PRELOAD into the top of the pin
    for s in (1,-1):
        x0,x1=sorted((s*a,s*b))
        S=S+(box(x0,x1,SPRING_ROOT-0.01,18.6,0,30)^slab(top-SPRING_T,top))
        S=S+(box(x0+0.3,x1-0.3,SEAT_Y-0.7,SEAT_Y+0.7,0,30)^slab(pad_c,top-SPRING_T+0.01))
    return S
def clear_of(S,parts,gap=0.15):
    for P in parts:
        for dx in (-gap,0,gap): S=S-P.translate([dx,0,0])
    return max(S.decompose(),key=lambda d:d.volume())
def build():
    shell=to_man(tm('top_shell'))
    R=new_button(xf(to_man(tm('right_button')),A_R),'R',shell)
    Lb=new_button(xf(to_man(tm('left_button')),A_L),'L',shell)
    St=spring_fingers(clear_of(new_stop(shell,tm('button_stop')),[R,Lb]))
    return shell,R,Lb,St
def export(outdir):
    import os
    os.makedirs(outdir,exist_ok=True)
    shell,R,Lb,St=build()
    for B,A,n in ((R,A_R,'right_button'),(Lb,A_L,'left_button')):      # simplify: the clearance cuts leave zero-volume flakes
        t=trimesh.load(trimesh.util.wrap_as_stream(to_tm(xf(B,inv(A)).simplify(0.0005)).export(file_type='stl')),file_type='stl')
        if not t.is_watertight:                                       # weld and drop the zero-area flakes the STL round trip exposes
            t.merge_vertices(digits_vertex=5); t.update_faces(t.nondegenerate_faces(height=1e-6)); t.update_faces(t.unique_faces())
            t.remove_unreferenced_vertices(); t=max(t.split(only_watertight=False),key=lambda c:len(c.faces))
        assert t.is_watertight, n
        t.export(os.path.join(outdir,n+'.stl'))
    # retainer: lay it on its flat inner face for printing
    P=St.rotate([np.degrees(np.arctan(SLOPE)),0,0]).rotate([0,180,0]); b=P.bounding_box()
    to_tm(P.translate([-(b[0]+b[3])/2,-(b[1]+b[4])/2,-b[2]])).export(os.path.join(outdir,'button_stop.stl'))
    return shell,R,Lb,St
def check(shell,R,Lb,St):
    base=to_man(tm('base')).transform(np.asarray(aff([[-1,0,0],[0,1,0],[0,0,-1]],[0,0,Z_BASE])[:3,:]))
    P={'right':R,'left':Lb,'retainer':St,'shell':shell,'base':base}; ks=list(P); bad=0
    def rot(M,deg): return M.translate([0,-SEAT_Y,-pin_z]).rotate([deg,0,0]).translate([0,SEAT_Y,pin_z])
    for i in range(len(ks)):
        for j in range(i+1,len(ks)):
            if {ks[i],ks[j]}=={'shell','base'}: continue
            v=(P[ks[i]]^P[ks[j]]).volume(); print(f'  {ks[i]:9s} x {ks[j]:9s} overlap {v:6.3f} mm3'+('  (spring preload)' if 'retainer' in (ks[i],ks[j]) and v>0 else '')); bad+=v>0.6
    for deg in (1.5,3.0):                      # press: front of the button swings toward the inside (+z)
        for k in ('right','left'):
            Bm=rot(P[k],deg); tip=np.radians(deg)*(COL_Y-SEAT_Y)
            for o in ks:
                if o==k: continue
                v=(Bm^P[o]).volume()
                if v>0.6: print(f'  pressed {deg} deg ({tip:.1f} mm at the striker): {k} x {o} overlap {v:.2f}',[np.round(d.bounding_box(),1).tolist() for d in (Bm^P[o]).decompose() if d.volume()>0.1][:3]); bad+=1
    print('problems:',bad); return bad
if __name__=='__main__':
    import sys
    check(*export(sys.argv[1] if len(sys.argv)>1 else MODELS))
