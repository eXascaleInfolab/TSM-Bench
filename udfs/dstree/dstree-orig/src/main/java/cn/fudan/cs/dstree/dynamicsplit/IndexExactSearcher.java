package cn.edu.fudan.cs.dstree.dynamicsplit;


import cn.edu.fudan.cs.dstree.util.CalcUtil;
import cn.edu.fudan.cs.dstree.util.DistUtil;
import cn.edu.fudan.cs.dstree.util.TimeSeriesFileUtil;
import cn.edu.fudan.cs.dstree.util.TimeSeriesReader;
import org.apache.commons.lang3.time.StopWatch;

import java.io.*;
import java.util.Comparator;
import java.util.Date;
import java.util.PriorityQueue;

/**
 * Created by IntelliJ IDEA.
 * User: ZhuShengqi
 * Date: 11-7-18
 * Time: 下午10:18
 * To change this template use File | Settings | File Templates.
 */
public class IndexExactSearcher {
    //classic exactFile
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        System.out.println("usage: java -cp uber-dstree-version.jar cn.edu.fudan.cs.dstree.dynamicsplit.IndexExactSearcher searchfilename indexdir");
        System.out.println("eg: java -cp uber-dstree-1.0-SNAPSHOT.jar cn.edu.fudan.cs.dstree.dynamicsplit.IndexExactSearcher data\\Series_64_1000000.z.search.txt data\\Series_64_1000000.z.txt.idx_dyn_100_1");

        String searchFileName = "data\\Series_64_1000000.z.search.txt";
        if (args.length >= 1)
            searchFileName = args[0];

        System.out.println("searchFileName = " + searchFileName);

        String indexPath = "data\\Series_64_1000000.z.txt.idx_dyn_100_1";
//        String indexPath = "data\\Series_64_1000000.z.txt.idx_dyn_100_1_10000";
        if (args.length >= 2)
            indexPath = args[1];

        System.out.println("indexPath = " + indexPath);

        search(searchFileName, indexPath);

    }

    public static Node approximateSearch(double[] queryTs, Node currentNode) {
        if (currentNode.isTerminal()) {
            return currentNode;
        } else //internal node
        {
            if (currentNode.splitPolicy.routeToLeft(queryTs))
                return approximateSearch(queryTs, currentNode.left);
            else
                return approximateSearch(queryTs, currentNode.right);
        }
    }

    public static void search(String searchFileName, String indexPath)
            throws IOException, ClassNotFoundException {
        String resultFileString = indexPath + ".search.log.txt";

        calcDistCount = 0;
        leafCount = 0;

        PrintWriter pw = new PrintWriter(new FileWriter(resultFileString));

        pw.println("indexPath = " + indexPath);
        File file = new File(indexPath);
        Node newRoot;
        if (file.exists()) {
            String indexFileName = indexPath + "\\" + "root.idx";
            System.out.println("reading idx fileName..." + indexFileName);
            pw.println("reading idx fileName..." + indexFileName);
//            FileInputStream fis = new FileInputStream(indexFileName);
//            ObjectInputStream ios = new ObjectInputStream(fis);
//            newRoot = (Node) ios.readObject();
            newRoot = Node.loadFromFile(indexFileName);
        } else {
            System.out.println("indexPath not exists! " + indexPath);
            pw.println("indexPath not exists! " + indexPath);
            return;
        }

        int tsLength = TimeSeriesFileUtil.getTimeSeriesLength(searchFileName);
        System.out.println("tsLength = " + tsLength);
        pw.println("tsLength = " + tsLength);

        System.out.println("threshold = " + newRoot.threshold);
        pw.println("threshold = " + newRoot.threshold);
//        newRoot.printTreeInfo();

        int totalTsCount = newRoot.getSize();
        System.out.println("totalTsCount = " + totalTsCount);
        pw.println("totalTsCount = " + totalTsCount);

        pw.println("---------------Exact search-----------------" + new Date());
        int searchCount = (int) TimeSeriesFileUtil.getTimeSeriesCount(new File(searchFileName));
        System.out.println("searchCount = " + searchCount);
        pw.println("searchCount = " + searchCount);
        double[] leafCounts = new double[searchCount];
        double[] proneRatios = new double[searchCount];

        TimeSeriesReader timeSeriesReader = new TimeSeriesReader(searchFileName);
        timeSeriesReader.open();
        int c = 0;

        totalTime.reset();
        totalTime.start();
        totalTime.suspend();
        ioTime.reset();
        ioTime.start();
        ioTime.suspend();
        approTime.reset();
        approTime.start();
        approTime.suspend();

        while (timeSeriesReader.hasNext()) {
            c++;
            System.out.println("************   " + (c) + "   ******************" + new Date());
            pw.println("************   " + c + "   ******************" + new Date());
            double[] queryTs = timeSeriesReader.next();
            totalTime.resume();
            Node node = exactSearch(queryTs, newRoot);
            totalTime.suspend();
            System.out.println("node.level = " + node.level);
            System.out.println("node.size = " + node.size);
            leafCounts[c - 1] = leafCount;
            proneRatios[c - 1] = (1 - calcDistCount * 1.0 / totalTsCount);
            System.out.println("leafCount = " + leafCount);
            pw.println("leafCount = " + leafCount);
            System.out.println("calcDistCount = " + calcDistCount);
            pw.println("calcDistCount = " + calcDistCount);
            System.out.println("proneRatios[c-1] = " + proneRatios[c - 1]);
            pw.println("proneRatios[c-1] = " + proneRatios[c - 1]);
        }
        timeSeriesReader.close();

        totalTime.stop();
        ioTime.stop();
        approTime.stop();

        System.out.println("*********** statistics for exact search **********");
        pw.println("avg(leafCounts) = " + CalcUtil.avg(leafCounts));
        System.out.println("avg(leafCounts) = " + CalcUtil.avg(leafCounts));
        pw.println("avg(proneRatios) = " + CalcUtil.avg(proneRatios));
        System.out.println("avg(proneRatios) = " + CalcUtil.avg(proneRatios));
        pw.println("ExactSearch TotalTime = " + totalTime.getTime() / 1000 + "s");
        System.out.println("ExactSearch TotalTime = " + totalTime.getTime() / 1000 + "s");
        pw.println("ExactSearch ApproximateSearchTime = " + approTime.getTime() / 1000 + "s");
        System.out.println("ExactSearch ApproximateSearchTime = " + approTime.getTime() / 1000 + "s");
        pw.println("ExactSearch IOTime = " + ioTime.getTime() / 1000 + "s");
        System.out.println("ExactSearch IOTime = " + ioTime.getTime() / 1000 + "s");
        long locationTime = (totalTime.getTime() - ioTime.getTime()) / 1000;
        pw.println("ExactSearch LocationTime = " + locationTime + "s");
        System.out.println("ExactSearch LocationTime = " + locationTime + "s");
        pw.close();
    }

    static int calcDistCount = 0;
    static int leafCount = 0;
    static StopWatch totalTime = new StopWatch();
    static StopWatch ioTime = new StopWatch();
    static StopWatch approTime = new StopWatch();

    public static Node  exactSearch(double[] queryTs, Node root) throws IOException {
        leafCount = 0;
        calcDistCount = 0;
        int processTerminalCount = 0;
        approTime.resume();
        Node approxNode = approximateSearch(queryTs, root);
        approTime.suspend();
        //get estimate lower bound from root
        PqItem bsfAnswer = new PqItem();
        bsfAnswer.node = approxNode;
        bsfAnswer.dist = DistUtil.minDistBinary(approxNode.getFileName(), queryTs);

        System.out.println("bsf.node = " + bsfAnswer.node.getFileName());
        System.out.println("bsf.dist = " + bsfAnswer.dist);
        //initialize priority queue;
        Comparator<PqItem> comparator = new DistComparator();
        PriorityQueue<PqItem> pq = new PriorityQueue<PqItem>(256, comparator);

        //initialize the priority queue
        PqItem tempItem = new PqItem();
        tempItem.node = root;
        tempItem.dist = DistTools.minDist(root, queryTs);
        pq.add(tempItem);

        //process the priority queue
        PqItem minPqItem;
        while (!pq.isEmpty()) {
            minPqItem = pq.remove();
            if (minPqItem.dist > bsfAnswer.dist) break;
            if (minPqItem.node.isTerminal()) {
                leafCount++;
                //verify the true distance,replace the estimate with the true dist
                calcDistCount += minPqItem.node.getSize();
                processTerminalCount++;
//                ioTime.resume();
//                minPqItem.dist = DistTools.IndexDist(minPqItem.node, queryTs);

                String fileName = minPqItem.node.getFileName();
                ioTime.resume();
//                double[][] tss = TimeSeriesFileUtil.readSeriesFromFileAtOnce(fileName);
                double[][] tss = TimeSeriesFileUtil.readSeriesFromBinaryFileAtOnce(fileName, queryTs.length);

//                double[][] tss = TimeSeriesFileUtil.readSeriesFromFile(fileName);
                ioTime.suspend();
                minPqItem.dist = DistUtil.minDist(tss, queryTs);

                //EuclideanCounter += minPqItem.node.amount;
                if (bsfAnswer.dist >= minPqItem.dist) {
                    bsfAnswer.dist = minPqItem.dist;
                    bsfAnswer.node = minPqItem.node;
                }
            } else {     //minPqItem is internal
                //for left
                tempItem = new PqItem();
                tempItem.node = minPqItem.node.left;
                tempItem.dist = DistTools.minDist(tempItem.node, queryTs);

                if (tempItem.dist < bsfAnswer.dist)
                    pq.add(tempItem);

                //for right
                tempItem = new PqItem();
                tempItem.node = minPqItem.node.right;
                tempItem.dist = DistTools.minDist(tempItem.node, queryTs);

                if (tempItem.dist < bsfAnswer.dist)
                    pq.add(tempItem);
            }
        }

        // Evalueate minimum distances...
        pq.clear();
        tempItem = new PqItem();
        tempItem.node = root;
        tempItem.dist = DistTools.minDist(root, queryTs);
        pq.add(tempItem);


        System.out.println("exact search node = " + bsfAnswer.node.getFileName());
        System.out.println("exact search dist = " + bsfAnswer.dist);
        System.out.println("calcDistCount = " + calcDistCount);
        System.out.println("processTerminalCount = " + processTerminalCount);
        System.out.println("time = " + totalTime.getTime());
        return bsfAnswer.node;
    }
}
