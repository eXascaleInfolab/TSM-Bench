package cn.edu.fudan.cs.dstree.dynamicsplit;


import cn.edu.fudan.cs.dstree.util.TimeSeriesFileUtil;
import cn.edu.fudan.cs.dstree.util.TimeSeriesReader;

import java.io.File;
import java.io.IOException;

public class BoundSearcher {
    public static double calculateBound(double [] queryTs, double[] dataTs, Node root) throws IOException {
        // Given a query and a data point we find the data point's node and calculate this node's
        // Lower bound to the query
        Node dataTsNode = IndexExactSearcher.exactSearch(dataTs, root) ;
        return DistTools.minDist(dataTsNode, queryTs);
    }

    public static void main(String args[]) throws ClassNotFoundException, IOException {
        IndexExactSearcher.totalTime.reset();
        IndexExactSearcher.totalTime.start();
        IndexExactSearcher.totalTime.suspend();
        IndexExactSearcher.ioTime.reset();
        IndexExactSearcher.ioTime.start();
        IndexExactSearcher.ioTime.suspend();
        IndexExactSearcher.approTime.reset();
        IndexExactSearcher.approTime.start();
        IndexExactSearcher.approTime.suspend();
        String indexPath = args[0];
        String queryFile = args[1];
        String dataFile = args[2];

        File file = new File(indexPath);

        // Read query from file
        TimeSeriesReader queryTimeSeriesReader = new TimeSeriesReader(queryFile);
        queryTimeSeriesReader.open();
        double queryTs[];
        if(queryTimeSeriesReader.hasNext()) {
            queryTs = queryTimeSeriesReader.next();
            queryTimeSeriesReader.close();
        }
        else {
            System.out.println("Query file empty!!!");
            return;
        }

        Node root;
        if (file.exists()) {
            String indexFileName = indexPath + "\\" + "root.idx";
            System.out.println("reading idx fileName..." + indexFileName);
            System.out.println("reading idx fileName..." + indexFileName);
            root = Node.loadFromFile(indexFileName);
        } else {
            System.out.println("indexPath not exists! " + indexPath);
            System.out.println("indexPath not exists! " + indexPath);
            return;
        }



        // Each data file record is used as a query we find the node
        // and calculate its bound to the query file record.
        int tsLength = TimeSeriesFileUtil.getTimeSeriesLength(dataFile);
        TimeSeriesReader timeSeriesReader = new TimeSeriesReader(dataFile);
        timeSeriesReader.open();
        while (timeSeriesReader.hasNext()) {
            double dataTs[] = timeSeriesReader.next();
            double minDist = calculateBound(queryTs, dataTs, root);
            System.out.println("bound = " + minDist);
        }

    }
}
