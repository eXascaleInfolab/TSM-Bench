package cn.edu.fudan.cs.dstree.util.system;

import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
import java.lang.management.MemoryPoolMXBean;
import java.lang.management.RuntimeMXBean;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Used to get management information about the runtime environment.
 * <p/>
 * NOTE: do not instantiate this object when running in a 1.4 or lower JVM.
 */
public class RuntimeInformationBean implements RuntimeInformation {
    private final MemoryMXBean memoryBean;
    private final RuntimeMXBean runtimeBean;

    public RuntimeInformationBean() {
        memoryBean = ManagementFactory.getMemoryMXBean();
        runtimeBean = ManagementFactory.getRuntimeMXBean();
    }

    public long getTotalHeapMemory() {
        return memoryBean.getHeapMemoryUsage().getMax();
    }

    public long getTotalHeapMemoryUsed() {
        return memoryBean.getHeapMemoryUsage().getUsed();
    }

    public List<MemoryInformation> getMemoryPoolInformation() {
        List<MemoryPoolMXBean> mxBeans = ManagementFactory.getMemoryPoolMXBeans();
        List<MemoryInformation> result = new ArrayList<MemoryInformation>(mxBeans.size());
        for (MemoryPoolMXBean mxBean : mxBeans) {
            result.add(new MemoryInformationBean(mxBean));
        }
        return Collections.unmodifiableList(result);
    }

    public long getTotalPermGenMemory() {
        return getPermGen().getTotal();
    }

    public long getTotalPermGenMemoryUsed() {
        return getPermGen().getUsed();
    }


    public long getTotalNonHeapMemory() {
        return memoryBean.getNonHeapMemoryUsage().getMax();
    }

    public long getTotalNonHeapMemoryUsed() {
        return memoryBean.getNonHeapMemoryUsage().getUsed();
    }

    public String getJvmInputArguments() {
        final StringBuilder sb = new StringBuilder();
        for (final String argument : runtimeBean.getInputArguments()) {
            sb.append(argument).append(" ");
        }
        return sb.toString();
    }

    private MemoryInformation getPermGen() {
        for (final MemoryInformation info : getMemoryPoolInformation()) {
            final String name = info.getName().toLowerCase();
            if (name.contains("perm gen")) {
                return info;
            }
        }
        return new MemoryInformation() {

            public String getName() {
                return "";
            }

            public long getTotal() {
                return -1;
            }

            public long getUsed() {
                return -1;
            }

            public long getFree() {
                return -1;
            }
        };
    }
}
