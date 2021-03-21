from simple_gen_model_run import instantiate_model, solve_instance, get_results

import logging
import grpc
from concurrent.futures import ThreadPoolExecutor
from optorun_pb2_grpc import add_OptoRunServiceServicer_to_server




def main(args=None):
    # instance = instantiate_model()
    # solve_instance(instance)

    # results_dict = get_results(instance)
    # print(results_dict)

    server = grpc.server(ThreadPoolExecutor(max_workers=1))
    add_OptoRunServiceServicer_to_server(OptopyServer(), server)
    port = 50051
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    # logger.info('Optopy server ready on port %r', port)
    server.wait_for_termination()

if __name__ == '__main__':
    main()