import click
import csv

@click.group()
def cli():
    pass

@cli.command()
@click.argument('start_node')
@click.argument('input_graph', type=click.Path(exists=True))
def traverse(start_node, input_graph):
    nodes = {}
    # import graph from csv
    with open(input_graph) as graphfile:
        reader = csv.DictReader(graphfile)
        for row in reader:
            dest_cost_tup = (row["destination"], float(row["cost"]), row["dest_ip"])
            if row["source"] in nodes:
                nodes[row["source"]].append(dest_cost_tup)
            else:
                nodes[row["source"]] = [dest_cost_tup]

    # initialize bellman-ford
    costs = {}
    for node in nodes:
        costs[node] = {"cost": "inf"}
    costs[start_node] = {"cost": 0, "via": "start", "ip":"localhost"}

    click.echo(",".join(costs))
    click.echo(",".join(str(value["cost"]) for value in costs.values()))

    # iterate v-1 times
    count = 0
    while(count < len(costs) - 1):
        for node in nodes:
            if costs[node]["cost"] != "inf":
                for tup in nodes[node]:
                    destination = tup[0]
                    ip = tup[2]
                    new_cost = costs[node]["cost"] + tup[1]
                    current_cost = costs[destination]["cost"]
                    if current_cost == "inf" or current_cost > new_cost:
                        costs[destination] = {
                            "cost": new_cost,
                            "via": node,
                            "ip": ip
                        }
        count += 1

        # print out current iteration
        click.echo(",".join(str(value["cost"]) for value in costs.values()))

    click.echo("\n")

    # write final costs
    with open("out.csv", mode='w') as out_file:
        csv_writer = csv.writer(out_file)
        csv_writer.writerow(['dest', 'via', 'cost', 'dest_ip'])
        for node in costs:
            csv_writer.writerow([node, costs[node]["via"], costs[node]["cost"], costs[node]["ip"]])
    click.echo("\n".join("{}: {} via {}".format(key, str(value["cost"]), value["via"]) for (key, value) in costs.items()))

@cli.command()
@click.argument('dest_node')
def mtr(dest_node):
    nodes = {}
    # read in bellman ford output
    with open("out.csv") as graphfile:
        reader = csv.DictReader(graphfile)
        for row in reader:
            nodes[row["dest"]] = row

    paths = [nodes[dest_node]]
    # append destination to path
    while (paths[0]["via"] != "bellman-ford"):
        paths.insert(0, nodes[paths[0]["via"]])
    # print path
    click.echo("\n".join("{}.\t{}\t{}\t{}ms".format(index+1,path["via"], path["dest_ip"], path["cost"]) for (index,path) in enumerate(paths)))

if __name__ == "__main__":
    cli()
