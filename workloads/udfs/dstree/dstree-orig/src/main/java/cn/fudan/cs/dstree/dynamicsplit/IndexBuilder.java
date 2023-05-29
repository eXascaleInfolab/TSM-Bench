package cn.edu.fudan.cs.dstree.dynamicsplit;


import cn.edu.fudan.cs.dstree.util.TimeSeriesFileUtil;
import cn.edu.fudan.cs.dstree.util.TimeSeriesReader;
import cn.edu.fudan.cs.dstree.util.system.SystemInfoUtils;
import cn.edu.fudan.cs.dstree.util.system.SystemInfoUtilsImpl;
import org.apache.commons.io.FileUtils;

import java.io.*;
import java.util.Date;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 11-4-27
 * Time: 下午9:18
 * To change this template use File | Settings | File Templates.
 */
public class IndexBuilder {
    /**
     * usage: IndexBuilder data\Series_64_1000000.z.txt 100 4
     *
     * @param args
     * @throws java.io.IOException
     * @throws ClassNotFoundException
     */
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        System.out.println("usage: java -jar uber-dstree-version.jar timeseriesfilename threshlod initsegmentsize");
        System.out.println("eg: java -jar uber-dstree-1.0-SNAPSHOT.jar data\\Series_64_1000000.z.txt 100 1");
        String fileName = "data\\Series_64_1000000.z.txt";
        if (args.length > 0)
            fileName = args[0];

        //threshold
        int threshold = 100;
        if (args.length > 1) {
            threshold = Integer.parseInt(args[1]);
        }

        //segmentSize start from 1
        int segmentSize = 1;
        if (args.length > 2) {
            segmentSize = Integer.parseInt(args[2]);
        }

        int maxTsCount = -1;
//        int maxTsCount = 10000;
        if (args.length > 3) {
            maxTsCount = Integer.parseInt(args[3]);
        }
        System.out.println("maxTsCount = " + maxTsCount);

		String indexPath = null;
        if (args.length > 4) {
            indexPath = args[4];
        }
        System.out.println("indexPath = " + indexPath);


	
        SystemInfoUtils systemInfoUtils = new SystemInfoUtilsImpl();
        double bufferedMemorySize = systemInfoUtils.getTotalMemory() * 0.6;    //0.6 for buffer
        //double bufferedMemorySize = systemInfoUtils.getTotalMemory() * 0.6;    //0.6 for buffer
        System.out.println("bufferedMemorySize = " + bufferedMemorySize);	
        buildIndex(fileName, indexPath, threshold, segmentSize, bufferedMemorySize, maxTsCount);
        System.out.println("Finished!!!");

    }

    public static void buildIndex(String fileName, int threshold, int segmentSize, double bufferedMemorySize) throws IOException, ClassNotFoundException {
        buildIndex(fileName, null, threshold, segmentSize, bufferedMemorySize, -1);
    }

    public static void buildIndex(String fileName, String indexPath, int threshold, int segmentSize, double bufferedMemorySize, int maxTsCount) throws IOException, ClassNotFoundException {
        int tsLength = TimeSeriesFileUtil.getTimeSeriesLength(fileName);
        FileBufferManager.fileBufferManager = null;
        FileBufferManager.getInstance().tsLength = tsLength;
        FileBufferManager.getInstance().setBufferedMemorySize(bufferedMemorySize);
        FileBufferManager.getInstance().setThreshold(threshold);

        //init indexPath if null
        if (indexPath == null)
            indexPath = fileName;
        indexPath = indexPath + ".idx_dyn";
        indexPath = indexPath + "_" + threshold + "_" + segmentSize;
        if (maxTsCount > 0) {
            indexPath = indexPath + "_" + maxTsCount;
        }
        System.out.println("indexPath = " + indexPath);
        String resultFile = indexPath + "_result.txt";
        PrintWriter pw = new PrintWriter(new FileWriter(resultFile));
        pw.println("start at: " + new Date());
        File file = new File(indexPath);
        if (file.exists()) {
            pw.println("indexPath: " + indexPath + " exists! cleaning...");
            System.out.println("indexPath: " + indexPath + " exists! cleaning...");
            FileUtils.cleanDirectory(file);
        } else {
            boolean b = file.mkdirs();
            if (b) {
                pw.println("successfully create " + indexPath);
            } else {
                pw.println("fail to create " + indexPath);
            }
        }

        pw.println("fileName = " + fileName);
        pw.println("tsLength = " + tsLength);
        pw.println("threshold = " + threshold);
        pw.println("indexPath = " + indexPath);
        pw.println("segmentSize = " + segmentSize);

        Node root = new Node(indexPath, threshold);

        //init helper class instances
        INodeSegmentSplitPolicy[] nodeSegmentSplitPolicies = new INodeSegmentSplitPolicy[2];
        nodeSegmentSplitPolicies[0] = new MeanNodeSegmentSplitPolicy();
        nodeSegmentSplitPolicies[1] = new StdevNodeSegmentSplitPolicy();
        root.setNodeSegmentSplitPolicies(nodeSegmentSplitPolicies);

        MeanStdevSeriesSegmentSketcher seriesSegmentSketcher = new MeanStdevSeriesSegmentSketcher();
        root.setSeriesSegmentSketcher(seriesSegmentSketcher);
        root.setNodeSegmentSketchUpdater(new MeanStdevNodeSegmentSketchUpdater(seriesSegmentSketcher));

        root.setRange(new MeanStdevRange());

        //calc the split points by segmentSize
        short[] points = calcPoints(tsLength, segmentSize);
        root.initSegments(points);

        int count = 0;
        TimeSeriesReader timeSeriesReader = new TimeSeriesReader(fileName);
        timeSeriesReader.open();

        while (timeSeriesReader.hasNext()) {
            root.insert(timeSeriesReader.next());
            count++;
            if (count % 10000 == 0)
                System.out.println(new Date() + " count = " + count);
            if (maxTsCount > 0) {
                if (count >= maxTsCount)
                    break;
            }
        }
        timeSeriesReader.close();
        FileBufferManager.getInstance().saveAllToDisk();

        String indexFileName = indexPath + "\\" + "root.idx";
        pw.println("writing idx fileName..." + indexFileName);

        root.saveToFile(indexFileName);
//        FileOutputStream fos = new FileOutputStream(indexFileName);
//        ObjectOutputStream oos = new ObjectOutputStream(fos);
//        oos.writeObject(root);
//        fos.close();

        pw.println("reading idx fileName..." + indexFileName);
        File indexFile = new File(indexFileName);
        pw.println("IndexFile Size = " + indexFile.length() / 1048576 + "M");
        Node newRoot = Node.loadFromFile(indexFileName);

        //FileInputStream fis = new FileInputStream(indexFile);
        //ObjectInputStream ios = new ObjectInputStream(fis);
        //Node newRoot = (Node) ios.readObject();
        TreeInfo tInfo = newRoot.printTreeInfo();
        pw.println("TotalNodeCount = " + tInfo.getTotalCount());
        pw.println("TotalTimeSeriesCount = " + tInfo.getTsCount());
        pw.println("EmptyTerminalNodeCount = " + tInfo.getEmptyNodeCount());
        pw.println("noneEmptyTerminalNodeCount = " + tInfo.getNoneEmptyNodeCount());
        pw.println("avgPerNode = " + tInfo.getAvgPerNode());
        pw.println("avgLevel = " + tInfo.getAvgLevel());

        System.out.println("FileBufferManager.getInstance().ioRead = " + FileBufferManager.getInstance().ioRead);
        System.out.println("FileBufferManager.getInstance().ioWrite = " + FileBufferManager.getInstance().ioWrite);
        System.out.println("FileBufferManager.getInstance().ioDelete = " + FileBufferManager.getInstance().ioDelete);
        pw.println("FileBufferManager.getInstance().ioRead = " + FileBufferManager.getInstance().ioRead);
        pw.println("FileBufferManager.getInstance().ioWrite = " + FileBufferManager.getInstance().ioWrite);
        pw.println("FileBufferManager.getInstance().ioDelete = " + FileBufferManager.getInstance().ioDelete);
        //write the tree info into xml
        StringBuffer xml = new StringBuffer();
        root.toXml(xml);
        System.out.println("xml = \n" + xml);

//        String xmlFileName = indexPath + "\\" + "root.xml";
//        FileUtils.writeStringToFile(new File(xmlFileName), xml.toString());
        pw.println("Build the index successfully!!! at:" + new Date());
        pw.close();
    }

    public static short[] calcPoints(int tsLength, int segmentSize) {
        int avgLegnth = tsLength / segmentSize;
        short[] points = new short[segmentSize];
        for (int i = 0; i < points.length; i++) {
            points[i] = (short) ((i + 1) * avgLegnth);
        }

        //set the last one
        points[points.length - 1] = (short) tsLength;
        return points;
    }
}
