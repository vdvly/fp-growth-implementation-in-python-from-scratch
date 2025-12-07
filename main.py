import csv
from FpGrowth import fpgrowth, build_fp_tree
from HashTable import ChainHashMap
from FPTree import FP_Tree, Fp_node
import os

def load_csv_data(filepath, separator=','):
    """
    Loads transaction data from the sparse binary matrix format 
    (Item names in header, 1s/0s in data rows).
    """
    transactions = []
    
    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=separator)
            
            # 1. Read the Header Row (Item Names)
            try:
                # Store the column headers (item names)
                item_names = [name.strip() for name in next(reader) if name.strip()]
            except StopIteration:
                print("❌ Error: CSV file is empty.")
                return []
            
            # 2. Read Data Rows (Transactions)
            for row in reader:
                current_transaction = []
                
                # Iterate through the row, associating data cells with item names
                # We use zip(item_names, row) to pair the item name with its binary value
                for item_name, value in zip(item_names, row):
                    
                    # Check if the item is present (value is '1' or 1)
                    if value.strip() == '1':
                        current_transaction.append(item_name)
                
                if current_transaction:
                    transactions.append(current_transaction)
                    
        print(f"Loaded {len(transactions)} transactions from {filepath}")
        return transactions

    except Exception as e:
        print(f"❌ An error occurred during file loading: {e}")
        return []

if __name__ == "__main__":
    DATA_FILE = "market.csv"
    MIN_SUPPORT_COUNT = 100
    
    transactions = load_csv_data(DATA_FILE, separator=';')
    print("\n" + "=" * 60)
    print("FP-GROWTH MARKET BASKET ANALYSIS")
    print("=" * 60)
    print(f"Total Transactions: {len(transactions)}")
    print(f"Minimum Support Count: {MIN_SUPPORT_COUNT}")
    print("=" * 60)

    print("\n📊 Building FP-Tree...")
    fp_tree = build_fp_tree(transactions, MIN_SUPPORT_COUNT)

    if fp_tree:
        print("\n" + "─" * 60)
        print("FP-TREE STRUCTURE")
        print("─" * 60)
        fp_tree.root.display()
        
        print("\n" + "─" * 60)
        print("HEADER TABLE")
        print("─" * 60)
        print(f"{'Item':<20} | {'Count':<10} | {'Occurrences':<12}")
        print("─" * 60)
        for item in fp_tree.header_table:
            count, nodes = fp_tree.header_table[item]
            print(f"{str(item):<20} | {count:<10} | {len(nodes):<12}")

        print("\n🔍 Mining Frequent Itemsets...")
        frequent_itemsets = fpgrowth(transactions, MIN_SUPPORT_COUNT)
        
        print("\n" + "=" * 60)
        print("FREQUENT ITEMSETS RESULTS")
        print("=" * 60)
        frequent_itemsets.sort(key=lambda x: (len(x[0]), x[1], str(x[0])))

        for idx, (itemset, support) in enumerate(frequent_itemsets, 1):
            print(f"{idx:3d}. {str(set(itemset)):<35} → Support: {support}")
        
        print("=" * 60)
    else:
        print("❌ No frequent items found.")