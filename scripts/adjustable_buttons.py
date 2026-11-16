#!/usr/bin/env python3
"""Build the v2 buttons and retainer from the v1 parts in models/v1: screw-adjustable strikers and a low-play hinge.

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
FINGER_GAP=0.08                      # retainer fingers sit this far above the pins when the plate is screwed down hard
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
    B=B+((col+web)-roof)
    B=B-cyl(sx,COL_Y,COL_BOT-8.0,COL_BOT+1,1.35)
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
def clear_of(S,parts,gap=0.15):
    for P in parts:
        for dx in (-gap,0,gap): S=S-P.translate([dx,0,0])
    return max(S.decompose(),key=lambda d:d.volume())
def build():
    shell=to_man(tm('top_shell'))
    R=new_button(xf(to_man(tm('right_button')),A_R),'R',shell)
    Lb=new_button(xf(to_man(tm('left_button')),A_L),'L',shell)
    St=clear_of(new_stop(shell,tm('button_stop')),[R,Lb])
    return shell,R,Lb,St
def export(outdir):
    import os
    os.makedirs(outdir,exist_ok=True)
    shell,R,Lb,St=build()
    to_tm(xf(R,inv(A_R))).export(os.path.join(outdir,'right_button.stl'))
    to_tm(xf(Lb,inv(A_L))).export(os.path.join(outdir,'left_button.stl'))
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
            v=(P[ks[i]]^P[ks[j]]).volume(); print(f'  {ks[i]:9s} x {ks[j]:9s} overlap {v:6.3f} mm3'); bad+=v>0.6
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
