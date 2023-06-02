package cn.edu.fudan.cs.dstree.dynamicsplit;

import java.io.IOException;
import java.util.*;

/**
 * Created with IntelliJ IDEA.
 * User: wangyang
 * Date: 13-3-17
 * Time: 下午5:14
 * To change this template use File | Settings | File Templates.
 */
public class FileBufferManager {
    private long maxBufferedSize = 1000 * 1000 * 100; //
    private double bufferedMemorySize = 1024; //in megabtyes
    private long startTime;
    private int threshold;   //use to calc the priority  of remove
    int tsLength;
    int ioWrite = 0;
    int ioRead = 0;
    int ioDelete = 0;

    private long currentCount = 0;

    public long getStartTime() {
        return startTime;
    }

    public void setStartTime(long startTime) {
        this.startTime = startTime;
    }

    public void addCount(long count) {
        currentCount = currentCount + count;
    }

    public void removeCount(long count) {
        currentCount = currentCount - count;
    }

    public int getThreshold() {
        return threshold;
    }

    public void setThreshold(int threshold) {
        this.threshold = threshold;
    }

    public FileBufferManager() {
        startTime = System.currentTimeMillis();
    }

    public double getBufferedMemorySize() {
        return bufferedMemorySize;
    }

    protected FileBuffer createFileBuffer() {
        FileBuffer fileBuffer = new FileBuffer(this);
        return fileBuffer;
    }

    public void setBufferedMemorySize(double bufferedMemorySize) {
        this.bufferedMemorySize = bufferedMemorySize;
        maxBufferedSize = Math.round(bufferedMemorySize * 1024 * 1024 / 8);
        batchRemoveSize = maxBufferedSize / 2;
        //maxBufferedSize = 50000;	
	//       batchRemoveSize = 48227;
        System.out.println("bufferedMemorySize = " + bufferedMemorySize);
        System.out.println("maxBufferedSize = " + maxBufferedSize);
        System.out.println("batchRemoveSize = " + batchRemoveSize);
        System.out.println("batchRemoveTsCount = " + batchRemoveSize / tsLength);
    }

    public long batchRemoveSize = maxBufferedSize / 100;   //batch remove 1/100
    //public long batchRemoveSize = 48227;


    HashMap<String, FileBuffer> fileMap = new HashMap<String, FileBuffer>();

    public FileBuffer getFileBuffer(String fileName) throws IOException {
        if (!fileMap.containsKey(fileName)) {
            //do LRU remove
            if (currentCount >= maxBufferedSize) {
                System.out.println(new Date() + "batch remove ! " + batchRemoveSize);
                long toSize = maxBufferedSize - batchRemoveSize;
                ArrayList<FileBuffer> list = new ArrayList<FileBuffer>(fileMap.values());

//                long validStartTime = System.currentTimeMillis();
//                for (int i = 0; i < list.size(); i++) {
//                    FileBuffer fileBuffer = list.get(i);
//                    if (fileBuffer.getBufferCount() > 0 && fileBuffer.lastTouched < validStartTime)
//                        validStartTime = fileBuffer.lastTouched;
//                }
//
//                System.out.println("startTime = " + startTime);
//                startTime = validStartTime;
//                System.out.println("validStartTime = " + validStartTime);

                Collections.sort(list);
                int idx = 0;
                int bufferCount = list.get(idx).getBufferCount();
                System.out.println("bufferCount = " + bufferCount);
                while (currentCount > toSize) {
                    FileBuffer fileBuffer = list.get(idx);
                    flushBufferToDisk(fileBuffer.fileName);
                    idx++;
                }
                System.out.println(new Date() + "idx: " + idx);
                bufferCount = list.get(idx).getBufferCount();
                System.out.println("bufferCount = " + bufferCount);
            }

            FileBuffer fileBuffer = createFileBuffer();
            fileBuffer.fileName = fileName;
            fileMap.put(fileName, fileBuffer);
        }
        FileBuffer fileBuffer = fileMap.get(fileName);
        fileBuffer.lastTouched = System.currentTimeMillis();
        return fileBuffer;

    }

    public void saveAllToDisk() throws IOException {
        System.out.println("FileBufferManager.saveAllToDisk");
        Set<Map.Entry<String, FileBuffer>> entries = fileMap.entrySet();
        for (Iterator<Map.Entry<String, FileBuffer>> iterator = entries.iterator(); iterator.hasNext(); ) {
            Map.Entry<String, FileBuffer> next = (Map.Entry<String, FileBuffer>) iterator.next();
            next.getValue().flushBufferToDisk();
        }

    }

    public static FileBufferManager fileBufferManager;

    public static FileBufferManager getInstance() {
        if (fileBufferManager == null) {
            fileBufferManager = new FileBufferManager();
        }
        return fileBufferManager;
    }

    public void flushBufferToDisk(String fileName) throws IOException {
        FileBuffer fileBuffer = fileMap.get(fileName);
        fileBuffer.flushBufferToDisk();
    }

    public void DeleteFile(String fileName) {
        //call when do split
        FileBuffer fileBuffer = fileMap.get(fileName);
        fileBuffer.deleteFile();
        //delete file is never used anymore
        fileMap.remove(fileName);
    }

//    public
}
