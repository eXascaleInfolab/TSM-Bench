package cn.edu.fudan.cs.dstree.dynamicsplit;

import cn.edu.fudan.cs.dstree.util.TimeSeriesFileUtil;
import cn.edu.fudan.cs.dstree.util.TimeSeriesReader;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.Date;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 12-3-11
 * Time: 下午4:03
 * To change this template use File | Settings | File Templates.
 */
public class HistogramComparator {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        String searchFileName = "data\\Series_64_1000000.z.search.txt";
        if (args.length >= 1)
            searchFileName = args[0];
        System.out.println("searchFileName = " + searchFileName);

        String fileName = "data\\Series_64_1000000.z.txt";
        if (args.length >= 2)
            fileName = args[1];

        System.out.println("fileName = " + fileName);

        String indexPath = "data\\Series_64_1000000.z.txt.idx_dyn_100_1";
        if (args.length >= 3)
            indexPath = args[2];

        System.out.println("indexPath = " + indexPath);

        //int maxBuildCount = Integer.MAX_VALUE;
        int maxBuildCount = 1;
        if (args.length >= 4)
            maxBuildCount = Integer.parseInt(args[3]);

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

        int maxLevel = getMaxLevel(newRoot);
        System.out.println("maxLevel = " + maxLevel);
        int levelTestCount = 3;
        System.out.println("levelTestCount = " + levelTestCount);
	/*
        for (int i = 0; i < levelTestCount; i++) {
            int testLevel = (maxLevel * (i + 1)) / levelTestCount;
            System.out.println("testLevel = " + testLevel);
        }
	*/
        int testLevel = (maxLevel * 2) / levelTestCount;
        System.out.println("testLevel = " + testLevel);

	
        System.out.println("###################approximate histogram compare#################");

        int histSize = 20;

        TimeSeriesReader timeSeriesReader = new TimeSeriesReader(searchFileName);
        timeSeriesReader.open();
        int c = 0;
        while (timeSeriesReader.hasNext()) {
            c++;
            if (c > maxBuildCount) break;
            System.out.println("************   " + (c) + "   ******************");
            System.out.println("new Date() = " + new Date());

            double[] queryTs = timeSeriesReader.next();

            HistogramNode exactRoot = HistogramExactBuilder.build(queryTs, fileName);
            HistogramNode approxRoot = HistogramApproxBuilder.build(queryTs, newRoot);
            HistogramNode[] histogramNodes = new HistogramNode[levelTestCount];
	    /*
            for (int i = 0; i < histogramNodes.length; i++) {
                histogramNodes[i] = HistogramApproxBuilder.build(queryTs, newRoot, (maxLevel * (i + 1)) / levelTestCount);
            }
	    */
            histogramNodes[0] = HistogramApproxBuilder.build(queryTs, newRoot, (maxLevel * 2) / levelTestCount);
            System.out.println("approxRoot.lowBound = " + approxRoot.lowBound);
            System.out.println("approxRoot.uppBound = " + approxRoot.uppBound);
            System.out.println("exactRoot.lowBound = " + exactRoot.lowBound);
            System.out.println("exactRoot.uppBound = " + exactRoot.uppBound);

            double min = Math.min(approxRoot.lowBound, exactRoot.lowBound);
            double max = Math.max(approxRoot.uppBound, exactRoot.uppBound);

            Histogram exactHistogram = new Histogram(exactRoot, min, max, histSize);
            Histogram approxHistogram = new Histogram(approxRoot, min, max, histSize);

            Histogram[] approxHistograms = new Histogram[levelTestCount];
	    /*
            for (int i = 0; i < approxHistograms.length; i++) {
                approxHistograms[i] = new Histogram(histogramNodes[i], min, max, histSize);
            }
	    */
            approxHistograms[0] = new Histogram(histogramNodes[0], min, max, histSize);
            //print head
            System.out.print("bins\texact\tfull\t");
            for (int i = 0; i < levelTestCount; i++) {
                System.out.print((i+1) + "/" + levelTestCount + "\t");
            }
            System.out.println();

            //print data
	    /*
            for (int i = 0; i < approxHistogram.getCounts().length; i++) {
                System.out.print((formatter.format(exactHistogram.getStarts()[i] + exactHistogram.getStep() / 2)) + "\t" + exactHistogram.getCounts()[i] + "\t" + approxHistogram.getCounts()[i]);
                for (int j = 0; j < approxHistograms.length; j++) {
                    Histogram histogram = approxHistograms[j];
                    System.out.print("\t" + histogram.getCounts()[i]);
                }
                System.out.println();
            }
	    */
            for (int i = 0; i < approxHistogram.getCounts().length; i++) {
		Histogram histogram = approxHistograms[0];
		System.out.print("\t" + histogram.getCounts()[i]);
                System.out.println();
            }	    
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

    public static NumberFormat formatter = new DecimalFormat("#0.0000");
}
