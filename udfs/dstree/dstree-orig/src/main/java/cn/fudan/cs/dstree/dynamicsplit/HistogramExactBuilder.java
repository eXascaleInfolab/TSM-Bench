package cn.edu.fudan.cs.dstree.dynamicsplit;

import cn.edu.fudan.cs.dstree.util.DistUtil;
import cn.edu.fudan.cs.dstree.util.TimeSeriesFileUtil;
import cn.edu.fudan.cs.dstree.util.TimeSeriesReader;

import java.io.IOException;
import java.util.Date;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 12-3-11
 * Time: 下午3:03
 * To change this template use File | Settings | File Templates.
 */
public class HistogramExactBuilder {
    public static HistogramNode build(double[] queryTs, String fileName) throws IOException {
        double max = Double.NEGATIVE_INFINITY;
        double min = Double.POSITIVE_INFINITY;
        long count = 0;
        HistogramNode root = new HistogramNode(null, min, max, 0);
        int tsLength = TimeSeriesFileUtil.getTimeSeriesLength(fileName);
        if (tsLength != queryTs.length)
            throw new RuntimeException("time series size is not equal!!!");

        TimeSeriesReader timeSeriesReader = new TimeSeriesReader(fileName);
        timeSeriesReader.open();
        while (timeSeriesReader.hasNext()) {
            double[] ts = timeSeriesReader.next();
            double dist = DistUtil.euclideanDist(queryTs, ts);
            if (dist < min) min = dist;
            if (dist > max) max = dist;
            count ++;

            HistogramNode child = new HistogramNode(root,dist,dist,1);
            root.children.add(child);
        }
        timeSeriesReader.close();
        root.lowBound = min;
        root.uppBound = max;
        root.count = count;

        return root;
    }

    public static void main(String[] args) throws IOException {
        System.out.println("usage: java -cp uber-dstree-version.jar cn.edu.fudan.cs.dstree.dynamicsplit.HistogramExactBuilder searchfilename fileName [maxBuildCount]");
        System.out.println("eg: java -cp uber-dstree-1.0-SNAPSHOT.jar cn.edu.fudan.cs.dstree.dynamicsplit.HistogramExactBuilder data\\Series_64_1000000.z.search.txt data\\Series_64_1000000.z.txt 1");

        String searchFileName = "data\\Series_64_1000000.z.search.txt";
        if (args.length >= 1)
            searchFileName = args[0];

        System.out.println("searchFileName = " + searchFileName);

        String fileName = "data\\Series_64_1000000.z.txt";
        if (args.length >= 2)
            fileName = args[1];

        System.out.println("fileName = " + fileName);

//        int maxBuildCount = Integer.MAX_VALUE;
        int maxBuildCount = 1;
        if (args.length >= 3) {
            maxBuildCount = Integer.parseInt(args[2]);
        }

        if(maxBuildCount < Integer.MAX_VALUE) {
            System.out.println("maxBuildCount = " + maxBuildCount);
        }

        int histSize = 10;

        TimeSeriesReader timeSeriesReader = new TimeSeriesReader(searchFileName);
        timeSeriesReader.open();
        int c = 0;
        while (timeSeriesReader.hasNext()) {
            c++;
            if (c > maxBuildCount) break;
            System.out.println("************   " + (c) + "   ******************");
            System.out.println("new Date() = " + new Date());
            double[] queryTs = timeSeriesReader.next();
            HistogramNode root = build(queryTs, fileName);
            Histogram histogram = new Histogram(root,root.lowBound,root.uppBound, histSize);
            System.out.println("new Date() = " + new Date());
            histogram.printInfo();
        }
        timeSeriesReader.close();
    }
}
