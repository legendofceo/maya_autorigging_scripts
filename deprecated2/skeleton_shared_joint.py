import maya.cmds as cmds


class new():

    def __init__(self,id):
        self.id = id
        self.sym=None

    def set_rgb(self,rgb):        
        cmds.setAttr(self.id+'.overrideEnabled', 1)
        cmds.setAttr(self.id+'.overrideRGBColors', 1)
        cmds.setAttr(self.id+'.overrideColorR', rgb[0])
        cmds.setAttr(self.id+'.overrideColorG', rgb[1])
        cmds.setAttr(self.id+'.overrideColorB', rgb[2])
        cmds.setAttr(self.id+'.overrideShading', 0)
        if(self.sym!=None):
            self.sym.set_rgb(rgb)
        return self


    def set_sym(self,id):
        self.sym = new(id)
        return self

    def match_sym(self,right,left):
        cmds.matchTransform(self.id,right)
        cmds.matchTransform(self.sym.id,left)
        return self

    def pos_only(self):
        cmds.setAttr(self.id+'.rotateX',0)
        cmds.setAttr(self.id+'.rotateY',0)
        cmds.setAttr(self.id+'.rotateZ',0)
        cmds.setAttr(self.id+'.scaleX',1.0)
        cmds.setAttr(self.id+'.scaleY',1.0)
        cmds.setAttr(self.id+'.scaleZ',1.0)

        if(self.sym!=None):
            self.sym.pos_only()
        return self

    def set_tx(self,value):
        cmds.setAttr(self.id+'.translateX',value)
        if(self.sym!=None):
            self.sym.set_tx(value)
        return self

    def invert_socket(self):
        #right
        #left
        Z = 90+(90-cmds.getAttr(self.id+'.jointOrientZ'))

        Y = 0-(cmds.getAttr(self.id+'.jointOrientY')-180)

        cmds.setAttr(self.sym.id+'.jointOrientX',cmds.getAttr(self.id+'.jointOrientX')*-1)
        cmds.setAttr(self.sym.id+'.jointOrientY',cmds.getAttr(self.id+'.jointOrientY'))
        cmds.setAttr(self.sym.id+'.jointOrientZ',cmds.getAttr(self.id+'.jointOrientZ')*-1)
        cmds.setAttr(self.sym.id+'.rotateOrder',cmds.getAttr(self.id+'.rotateOrder'))
        cmds.setAttr(self.sym.id+'.translateX',cmds.getAttr(self.id+'.translateX'))
        cmds.setAttr(self.sym.id+'.translateY',cmds.getAttr(self.id+'.translateY')*-1)
        cmds.setAttr(self.sym.id+'.translateZ',cmds.getAttr(self.id+'.translateZ'))
        return self

    def invert_chain(self):
        #right
        #left

        cmds.setAttr(self.sym.id+'.jointOrientX',cmds.getAttr(self.id+'.jointOrientX'))
        cmds.setAttr(self.sym.id+'.jointOrientY',cmds.getAttr(self.id+'.jointOrientY'))
        cmds.setAttr(self.sym.id+'.jointOrientZ',cmds.getAttr(self.id+'.jointOrientZ')*-1)
        cmds.setAttr(self.sym.id+'.rotateOrder',cmds.getAttr(self.id+'.rotateOrder'))
        cmds.setAttr(self.sym.id+'.translateX',cmds.getAttr(self.id+'.translateX'))
        cmds.setAttr(self.sym.id+'.translateY',cmds.getAttr(self.id+'.translateY'))
        cmds.setAttr(self.sym.id+'.translateZ',cmds.getAttr(self.id+'.translateZ')*-1)
        return self

    def invert_free(self):
        cmds.setAttr(self.sym.id+'.jointOrientX',cmds.getAttr(self.id+'.jointOrientX'))
        cmds.setAttr(self.sym.id+'.jointOrientY',cmds.getAttr(self.id+'.jointOrientY'))
        cmds.setAttr(self.sym.id+'.jointOrientZ',cmds.getAttr(self.id+'.jointOrientZ'))
        cmds.setAttr(self.sym.id+'.rotateOrder',cmds.getAttr(self.id+'.rotateOrder'))
        cmds.setAttr(self.sym.id+'.translateX',cmds.getAttr(self.id+'.translateX'))
        cmds.setAttr(self.sym.id+'.translateY',cmds.getAttr(self.id+'.translateY')*-1)
        cmds.setAttr(self.sym.id+'.translateZ',cmds.getAttr(self.id+'.translateZ'))
        return self

    def x_only(self):
        cmds.setAttr(self.id+'.translateY', 0)
        cmds.setAttr(self.id+'.translateZ', 0)
        if(self.sym!=None):
            self.sym.x_only()
        return self

    def center(self):
        pos = cmds.xform(self.id,q=1,ws=1,t=1)
        if pos[0]!=0.0:
            print("CENTER NODE IS NOT CENTERED: "+self.id)
            print(pos)
        return self

    def label(self,value):
        cmds.setAttr(self.id+'.type', 18)
        cmds.setAttr(self.id+'.drawLabel', 1)
        cmds.setAttr(self.id+'.otherType', value,type='string')
        if(self.sym!=None):
            self.sym.label(value)
        return self

    def size(self,value):
        cmds.setAttr(self.id+'.radius', value) 
        if(self.sym!=None):
            self.sym.size(value)
        return self

    def lod(self,value):
        #0 = All
        #1 = 1 Only
        #2 = 1 And 2 Only
        if cmds.attributeQuery('lod',n=self.id,exists=True):
            cmds.deleteAttr(self.id+'.lod')
        cmds.addAttr(self.id, longName='lod', nn="LOD", attributeType='short',dv=value,max=3)
        if(self.sym!=None):
            self.sym.lod(value)
        return self

    def axis(self):
        #0 = Center
        #1 = Left
        #2 = Right
        #3 = Sin
        #4 = Dex
        #5 = None
        #if cmds.attributeQuery('jointaxis',n=self.id,exists=True):
        #    cmds.deleteAttr(self.id+'.jointaxis')
        #cmds.addAttr(self.id, longName='jointaxis', nn="Joint Axis", attributeType='short',dv=value,max=6)
        cmds.setAttr(self.id+".side",2)
        if(self.sym!=None):
            cmds.setAttr(self.sym.id+".side",1)
        return self

    def jexportanim(self,value):
        #0 = None
        #1 = Chain
        #2 = Free
        #3 = Socket
        if cmds.attributeQuery('exportanim',n=self.id,exists=True):
            cmds.deleteAttr(self.id+'.exportanim')
        cmds.addAttr(self.id, longName='exportanim', nn="Should Export With Animations", attributeType='bool', dv=value )
        if(self.sym!=None):
            self.sym.axis(value)
        return self

    def end(self,arr):
        arr.append(self.id)
        if(self.sym!=None):
            arr.append(self.sym.id)
        return self