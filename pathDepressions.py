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

def depressCrvs(crvs,paths,startPt,radius,sd):
    newCrvs = []
    for i in range(len(crvs)):
        divPts = rs.DivideCurve(crvs[i],100)
        if i<len(crvs)-1:
            cntPt01 = centerCrv(crvs[i])
            cntPt02 = centerCrv(crvs[i+1])
            horVec = rs.VectorCreate(cntPt01,cntPt02)
        for j in range(len(divPts)):
            path = rs.PointClosestObject(divPts[j],paths)[0]
            param = rs.CurveClosestPoint(path,divPts[j])
            close = rs.EvaluateCurve(path,param)
            dist = rs.Distance(close,divPts[j])
            tan = rs.CurveTangent(crvs[i],param)
            vec = [0,0,-1] #rs.VectorCrossProduct(horVec,tan)
            testVec = rs.VectorCreate(cntPt01,divPts[j])
            if rs.VectorDotProduct(vec,testVec)<0:
                rs.VectorReverse(vec)
            vec = rs.VectorUnitize(vec)
            border = 1
            entry = 1
            if j>len(divPts)/2:
                border = rs.Distance(rs.CurveEndPoint(crvs[i]),divPts[j])
            else:
                border = rs.Distance(rs.CurveStartPoint(crvs[i]),divPts[j])
            if border<sd*3:
                border = border/(sd*3)
            entryDist = rs.Distance(startPt,divPts[j])
            if entryDist<sd*3:
                entry = entryDist/(sd*5)
            if dist<sd*2:
                val = radius*(bellCrv(dist,sd))
                divPts[j] = rs.PointAdd(divPts[j],vec*val*border*entry)
        newCrvs.append(rs.AddCurve(divPts))
    return divPts

def Main():
    crvs= rs.GetObjects("please select curves",rs.filter.curve)
    paths= rs.GetObjects("please select depression paths",rs.filter.curve)
    startPt = rs.GetObject("please select entry point",rs.filter.point)
    radius = rs.GetReal("please enter path radius",.02)
    power = rs.GetReal("please enter standard dev",.5)
    crvs = depressCrvs(crvs,paths,startPt,radius,power)
    return crvs

Main()