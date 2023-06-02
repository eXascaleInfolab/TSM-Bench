package cn.edu.fudan.cs.dstree.dynamicsplit;

import cn.edu.fudan.cs.dstree.util.CalcUtil;
import cn.edu.fudan.cs.dstree.util.DistUtil;
import cn.edu.fudan.cs.dstree.util.TimeSeriesFileUtil;
import cn.edu.fudan.cs.dstree.util.TimeSeriesReader;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 11-4-28
 * Time: 上午12:46
 * To change this template use File | Settings | File Templates.
 */
public class IndexApproxSearcher {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        String searchFileName = "data\\Series_64_1000000.z.search.txt";
        if (args.length >= 1)
            searchFileName = args[0];

        System.out.println("searchFileName = " + searchFileName);

        String indexPath = "data\\Series_64_1000000.z.txt.idx_dyn_100_1";
        if (args.length >= 2)
            indexPath = args[1];

        System.out.println("indexPath = " + indexPath);

        File file = new File(indexPath);
        Node newRoot;
        if (file.exists()) {
            String indexFileName = indexPath + "\\" + "root.idx";
            System.out.println("reading idx fileName..." + indexFileName);
            newRoot = Node.loadFromFile(indexFileName);
        } else {
            System.out.println("indexPath not exists! " + indexPath);
            return;
        }

        int tsLength = TimeSeriesFileUtil.getTimeSeriesLength(searchFileName);
        System.out.println("tsLength = " + tsLength);

        System.out.println("threshold = " + newRoot.threshold);
//        newRoot.printTreeInfo();
        int totalTsCount = newRoot.getSize();

        System.out.println("###################approximate search#################");
        int searchCount = (int) TimeSeriesFileUtil.getTimeSeriesCount(new File(searchFileName));
        double[] levels = new double[searchCount];
        double[] lowBoundErrRatios = new double[searchCount];
        double[] lowBoundAvgErrRatios = new double[searchCount];
        double[] proneRatios = new double[searchCount];
        double[] approxErrRatios = new double[searchCount];

        TimeSeriesReader timeSeriesReader = new TimeSeriesReader(searchFileName);
        timeSeriesReader.open();
        int c = 0;
        while (timeSeriesReader.hasNext()) {
            System.out.println("************   " + (++c) + "   ******************");
            double[] queryTs = timeSeriesReader.next();
            Node node = newRoot.approximateSearch(queryTs);
            System.out.println("node.level = " + node.level);
            System.out.println("node.size = " + node.size);

            double lowBound = DistTools.minDist(node, queryTs);
            double lowBoundByAvg = DistTools.minDistByAvg(node, queryTs);
            System.out.println("lowBoundByAvg = " + lowBoundByAvg);
            System.out.println("lowBound = " + lowBound);

            //calc the min distance
            double minDist = DistUtil.minDistBinary(node.getFileName(), queryTs);
            System.out.println("minDist = " + minDist);

//            double bruteForceDist = DistUtil.minDist(fileName, queryTs);
//            System.out.println("bruteForceDist = " + bruteForceDist);

            levels[c - 1] = node.level;
            lowBoundErrRatios[c - 1] = (minDist - lowBound) / (minDist > 0 ? minDist : 0.1);
            lowBoundAvgErrRatios[c - 1] = (minDist - lowBoundByAvg) / (minDist > 0 ? minDist : 0.1);
            proneRatios[c - 1] = node.getSize() * 1.0 / totalTsCount;
//            approxErrRatios[c-1] = (minDist - bruteForceDist)/(bruteForceDist>0?bruteForceDist:0.1);
        }
        timeSeriesReader.close();

        System.out.println("*********** statistics for approximate search **********");
        System.out.println("avg(levels) = " + CalcUtil.avg(levels));
        System.out.println("avg(lowBoundErrRatios) = " + CalcUtil.avg(lowBoundErrRatios));
        System.out.println("avg(lowBoundAvgErrRatios) = " + CalcUtil.avg(lowBoundAvgErrRatios));
        System.out.println("avg(proneRatios) = " + CalcUtil.avg(proneRatios));
//        System.out.println("avg(approxErrRatios) = " + CalcUtil.avg(approxErrRatios));
    }

    public static void approximateSearch(Node newRoot, String searchFileName) throws IOException {
        TimeSeriesReader timeSeriesReader = new TimeSeriesReader(searchFileName);
        timeSeriesReader.open();
        while (timeSeriesReader.hasNext()) {
            double[] queryTs = timeSeriesReader.next();
            Node node = newRoot.approximateSearch(queryTs);
            System.out.println("node.level = " + node.level);
            System.out.println("node.size = " + node.size);
            //calc the min distance
            double minDist = DistUtil.minDist(node.getFileName(), queryTs);
            System.out.println("minDist = " + minDist);

//            System.out.println("******************************");
        }
        timeSeriesReader.close();
    }
}
