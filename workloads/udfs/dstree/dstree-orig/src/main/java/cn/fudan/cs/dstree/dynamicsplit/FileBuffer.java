package cn.edu.fudan.cs.dstree.dynamicsplit;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

/**
 * Created with IntelliJ IDEA.
 * User: wangyang
 * Date: 13-3-17
 * Time: 下午5:20
 * To change this template use File | Settings | File Templates.
 */
public class FileBuffer implements Comparable {
    public String fileName;
    private List<double[]> bufferedList = new ArrayList<double[]>();
    private boolean inDisk = false;
    public long lastTouched;

    private int diskCount = 0;

    public int getBufferCount() {
        return bufferedList.size();
    }

    public List<double[]> getAllTimeSeries() throws IOException {

        if (diskCount > 0) {
            List<double[]> ret = new ArrayList<double[]>();
            //load ts from disk;
            fileBufferManager.ioRead++;
            FileInputStream fis = new FileInputStream(fileName);
            BufferedInputStream bis = new BufferedInputStream(fis);
            DataInputStream dis = new DataInputStream(bis);


            for (int i = 0; i < diskCount; i++) {
                double[] ts = new double[fileBufferManager.tsLength];
                for (int j = 0; j < ts.length; j++) {
                    ts[j] = dis.readDouble();
                }
                ret.add(ts);
            }
            dis.close();
            bis.close();
            fis.close();
            ret.addAll(bufferedList);
            return ret;
        }

        return bufferedList;
    }

    public FileBuffer(FileBufferManager fileBufferManager) {
        this.fileBufferManager = fileBufferManager;
    }

    public int getTotalCount() {
        return diskCount + getBufferCount();
    }

    private FileBufferManager fileBufferManager;

    public void append(double[] ts) {
        bufferedList.add(ts);
        fileBufferManager.addCount(ts.length);
    }

    public void flushBufferToDisk() throws IOException {
        if (getBufferCount() > 0) {
            appendToFile();
        }
    }

    //do append appendToFile
    private void appendToFile() throws IOException {
        FileOutputStream fos = new FileOutputStream(fileName, true);

        BufferedOutputStream bos = new BufferedOutputStream(fos);
        DataOutputStream dos = new DataOutputStream(bos);
        for (int i = 0; i < bufferedList.size(); i++) {
            double[] ts = bufferedList.get(i);
            for (int j = 0; j < ts.length; j++)
                dos.writeDouble(ts[j]);
        }
        dos.close();
        bos.flush();
        bos.close();

        fileBufferManager.ioWrite++;
        //remove the ts  and adjust the fileBufferManager buffer count
        fileBufferManager.removeCount(bufferedList.size() * bufferedList.get(0).length);
        //update diskCount
        diskCount = diskCount + bufferedList.size();
        bufferedList.clear();

        inDisk = true;
    }

    public void deleteFile() {
        if (inDisk) {
            new File(fileName).delete();
            fileBufferManager.ioDelete++;
            diskCount = 0;
            inDisk = false;
        }
        //remove the ts  and adjust the fileBufferManager buffer count
        if (getBufferCount() > 0) {
            fileBufferManager.removeCount(bufferedList.size() * bufferedList.get(0).length);
            //update diskCount
            bufferedList.clear();
        }
    }

    public static long OneMinuteInMillis = 60 * 1000;

    public double p;

    private double priority() {
//        double notUsedTime = (lastTouched * 1.0 - fileBufferManager.getStartTime()) / OneMinuteInMillis;
//        p = notUsedTime + (getBufferCount() * 1) - 1.1 * (Math.abs(fileBufferManager.getThreshold() / 2.0 - getTotalCount()));
        return getBufferCount();// / (getTotalCount() + fileBufferManager.getThreshold()); //100 is adjust factory
    }

    public int compareTo(Object o) {
        //get time not used time in hour
        FileBuffer fileBuffer1 = (FileBuffer) o;
        return -1 * Double.compare(priority(), fileBuffer1.priority());
    }
}
