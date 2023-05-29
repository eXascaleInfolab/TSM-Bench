package cn.edu.fudan.cs.dstree.dynamicsplit;

public class TreeInfo {
    private int totalCount = 0;
    private int emptyNodeCount = 0;
    private int noneEmptyNodeCount = 0;
    private int tsCount = 0;
    private double avgLevel = 0;
    private double avgPerNode = 0;

    public int getTotalCount() {
        return totalCount;
    }

    public void setTotalCount(int totalCount) {
        this.totalCount = totalCount;
    }

    public int getEmptyNodeCount() {
        return emptyNodeCount;
    }

    public void setEmptyNodeCount(int emptyNodeCount) {
        this.emptyNodeCount = emptyNodeCount;
    }

    public int getNoneEmptyNodeCount() {
        return noneEmptyNodeCount;
    }

    public void setNoneEmptyNodeCount(int noneEmptyNodeCount) {
        this.noneEmptyNodeCount = noneEmptyNodeCount;
    }

    public int getTsCount() {
        return tsCount;
    }

    public void setTsCount(int tsCount) {
        this.tsCount = tsCount;
    }

    public double getAvgLevel() {
        return avgLevel;
    }

    public void setAvgLevel(double avgLevel) {
        this.avgLevel = avgLevel;
    }

    public double getAvgPerNode() {
        return avgPerNode;
    }

    public void setAvgPerNode(double avgPerNode) {
        this.avgPerNode = avgPerNode;
    }

}
