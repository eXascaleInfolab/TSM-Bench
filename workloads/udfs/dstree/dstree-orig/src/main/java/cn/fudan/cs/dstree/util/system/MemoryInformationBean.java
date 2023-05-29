package cn.edu.fudan.cs.dstree.util.system;

import java.lang.management.MemoryPoolMXBean;

public class MemoryInformationBean implements MemoryInformation {
    private final MemoryPoolMXBean memoryPool;

    MemoryInformationBean(final MemoryPoolMXBean memoryPool) {
        this.memoryPool = memoryPool;
    }

    public String getName() {
        return memoryPool.getName();
    }

    public long getTotal() {
        return memoryPool.getUsage().getMax();
    }

    public long getUsed() {
        return memoryPool.getUsage().getUsed();
    }

    public long getFree() {
        return getTotal() - getUsed();
    }

    @Override
    public String toString() {
        return memoryPool.getName() + ": " + memoryPool.getUsage();
    }
}
