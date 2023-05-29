package cn.edu.fudan.cs.dstree.dynamicsplit;

import cn.edu.fudan.cs.dstree.util.DistUtil;
import cn.edu.fudan.cs.dstree.util.TimeSeriesFileUtil;

import java.io.IOException;

/**
 * Created with IntelliJ IDEA.
 * User: wangyang
 * Date: 13-3-19
 * Time: 上午12:16
 * To change this template use File | Settings | File Templates.
 */
public class BruteForceExactSearcher {
    public static void main(String[] args) throws IOException {
        String fileName = args[0];
        String searchFileName = args[1];

        double[] dists = search(fileName, searchFileName);
        for (int i = 0; i < dists.length; i++) {
            double dist = dists[i];
            System.out.println("i = " + i);
            System.out.println("dist = " + dist);
        }
    }

    public static double[] search(String fileName, String searchFileName) throws IOException {
        double[][] multiTs = TimeSeriesFileUtil.readSeriesFromFile(searchFileName);
        return DistUtil.minDist(fileName, multiTs);
    }
}
