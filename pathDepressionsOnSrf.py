import rhinoscriptsyntax as rs
import math as m

def centerCrv(crv):
    sum = [0,0,0]
    pts = rs.DivideCurve(crv,1000)
    for i in range(len(pts)):
        sum = rs.PointAdd(sum,pts[i])
    cnt = sum/len(pts)
    return cnt

def bellCrv(val,sd):
    coefficent = 1/(sd*m.pow(2*m.pi,.5))
    power = -1*m.pow(val,2)/(2*m.pow(sd,2))
    y = coefficent*m.pow(m.e,power)
    return y

def depressCrvs(srf,crvs,paths,startPt,radius,sd):
    newCrvs = []
    for i in range(len(crvs)):
        divPts = rs.DivideCurve(crvs[i],400)
        for j in range(len(divPts)):
            path = rs.PointClosestObject(divPts[j],paths)[0]
            param = rs.CurveClosestPoint(path,divPts[j])
            close = rs.EvaluateCurve(path,param)
            srfParam = rs.SurfaceClosestPoint(srf,close)
            vec = rs.SurfaceNormal(srf,srfParam)
            dist = rs.Distance(close,divPts[j])
            vec = rs.VectorUnitize(vec)
            border = 1
            entry = 1
            if j>len(divPts)/2:
                border = rs.Distance(rs.CurveEndPoint(crvs[i]),divPts[j])
            else:
                border = rs.Distance(rs.CurveStartPoint(crvs[i]),divPts[j])
            if border<sd*3:
                border = border/(sd*3)
            else:
                border = 1
            entryDist = rs.Distance(startPt,divPts[j])
            if entryDist<sd*10:
                entry = entryDist/(sd*10)
            else:
                entry = 1
            if dist<sd*2:
                val = radius*(bellCrv(dist,sd))
                divPts[j] = rs.PointAdd(divPts[j],vec*val*border*entry)
        newCrvs.append(rs.AddCurve(divPts))
    return divPts

def Main():
    crvs= rs.GetObjects("please select srf curves",rs.filter.curve)
    paths= rs.GetObjects("please select depression paths",rs.filter.curve)
    startPt = rs.GetObject("please select entry point",rs.filter.point)
    radius = rs.GetReal("please enter path radius",2)
    sd = rs.GetReal("please enter standard dev",.25)
    srf = rs.GetObject("please enter surface", rs.filter.surface)
    crvs = depressCrvs(srf,crvs,paths,startPt,radius,sd)
    return crvs

Main()