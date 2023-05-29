package cn.edu.fudan.cs.dstree.dynamicsplit;

import cn.edu.fudan.cs.dstree.util.TimeSeriesReader;

import java.io.File;
import java.io.IOException;
import java.util.Date;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 12-3-11
 * Time: 下午3:30
 * To change this template use File | Settings | File Templates.
 */
public class HistogramApproxBuilder {

    public static HistogramNode build(double[] queryTs, Node indexRoot) throws IOException {
        return build(queryTs, indexRoot, Integer.MAX_VALUE);
    }

    public static HistogramNode build(double[] queryTs, Node indexRoot, int maxLevel) throws IOException {
        double max = Double.NEGATIVE_INFINITY;
        double min = Double.POSITIVE_INFINITY;
        HistogramNode root = new HistogramNode(null, min, max, 0);
        build(queryTs, root, indexRoot, maxLevel);
        return root;
    }

    private static void build(double[] queryTs, HistogramNode current, Node node, int maxLevel) throws IOException {
        double parent_low = Double.NEGATIVE_INFINITY;
        double parent_upp = Double.POSITIVE_INFINITY;

        //get the bounds by parent low and upp
        if (current.parent != null) {
            parent_low = current.parent.lowBound;
            parent_upp = current.parent.uppBound;
        }

        //modify the bounds if exceeds the parent bounds
        current.lowBound = Math.max(DistTools.minDist(node, queryTs), parent_low);
        current.uppBound = Math.min(DistTools.maxDist(node, queryTs), parent_upp);

        current.count = node.getSize();

        //deal with children if not reach maxLevel
        //        System.out.println("node.level = " + node.level);
        if (node.level >= maxLevel)
            return;

        //build recursively
        if (node.left != null && node.left.getSize() > 0) {
            HistogramNode left = new HistogramNode(current, 0, 0, 0);
            current.children.add(left);
            build(queryTs, left, node.left, maxLevel);
        }

        if (node.right != null && node.right.getSize() > 0) {
            HistogramNode right = new HistogramNode(current, 0, 0, 0);
            current.children.add(right);
            build(queryTs, right, node.right, maxLevel);
        }
    }

    public static void main(String[] args) throws IOException, ClassNotFoundException {
        String searchFileName = "data\\Series_64_1000000.z.search.txt";
        if (args.length >= 1)
            searchFileName = args[0];
        System.out.println("searchFileName = " + searchFileName);

        String indexPath = "data\\Series_64_1000000.z.txt.idx_dyn_100_1";
        if (args.length >= 2)
            indexPath = args[1];

        System.out.println("indexPath = " + indexPath);

        //int maxBuildCount = Integer.MAX_VALUE;
        int maxBuildCount = 1;
        if (args.length >= 3)
            maxBuildCount = Integer.parseInt(args[2]);

        if (maxBuildCount < Integer.MAX_VALUE)
            System.out.println("maxBuildCount = " + maxBuildCount);

        Node newRoot;
        File file = new File(indexPath);
        if (file.exists()) {
            String indexFileName = indexPath + "\\" + "root.idx";
            System.out.println("reading idx fileName..." + indexFileName);
            newRoot = Node.loadFromFile(indexFileName);
        } else {
            System.out.println("indexPath not exists! " + indexPath);
            return;
        }

        int histSize = 10;

        System.out.println("###################approximate histogram builder#################");
        TimeSeriesReader timeSeriesReader = new TimeSeriesReader(searchFileName);
        timeSeriesReader.open();
        int c = 0;
        //int maxLevel = Integer.MAX_VALUE;      //level not limited
        int maxLevel = getMaxLevel(newRoot)*2/3;
        System.out.println("maxLevel = " + maxLevel);
	
        while (timeSeriesReader.hasNext()) {
            c++;
            if (c > maxBuildCount) break;
            System.out.println("************   " + (c) + "   ******************");
            System.out.println("new Date() = " + new Date());
            long t1 = System.currentTimeMillis();
            double[] queryTs = timeSeriesReader.next();
            HistogramNode root = build(queryTs, newRoot, maxLevel);
	    //HistogramApproxBuilder.build(queryTs, newRoot, (maxLevel * (i + 1)) / levelTestCount)
            Histogram histogram = new Histogram(root, root.lowBound, root.uppBound, histSize);
            System.out.println("new Date() = " + new Date());
            histogram.printInfo();
            long t2 = System.currentTimeMillis();
            long timecost = (t2 - t1);
            System.out.println("timecost = " + timecost/1000.0);
        }
        timeSeriesReader.close();
    }
    
    private static int getMaxLevel(Node node) {
        if (node.isTerminal()) {
            return node.level;
        } else {
            return Math.max(getMaxLevel(node.left), getMaxLevel(node.right));
        }
    }
    
}
