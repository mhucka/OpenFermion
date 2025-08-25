#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import time
from urllib.error import URLError


def _get_from_pubchem_with_retries(retries=3, delay=1, **kwargs):
    """Get a compound from PubChem, retrying if the server is busy.

    Args:
        retries(int): The number of times to retry.
        delay(float): The delay between retries, in seconds.
        **kwargs: The arguments to pass to pubchempy.get_compounds.
    """
    import pubchempy

    for i in range(retries):
        try:
            return pubchempy.get_compounds(**kwargs)
        except URLError as e:
            if i < retries - 1:
                time.sleep(delay)
            else:
                raise e


def geometry_from_pubchem(name: str, structure: str = None):
    """Function to extract geometry using the molecule's name from the PubChem
    database. The 'structure' argument can be used to specify which structure
    info to use to extract the geometry. If structure=None, the geometry will
    be constructed based on 3D info, if available, otherwise on 2D (to keep
    backwards compatibility with the times when the argument 'structure'
    was not implemented).

    Args:
        name: a string giving the molecule's name as required by the PubChem
            database.
        structure: a string '2d' or '3d', to specify a specific structure
            information to be retrieved from pubchem. The default is None.
            Recommended value is '3d'.

    Returns:
        geometry: a list of tuples giving the coordinates of each atom with
        distances in Angstrom.
    """
    if structure in ['2d', '3d']:
        pubchempy_molecule = _get_from_pubchem_with_retries(
            identifier=name, namespace='name', record_type=structure
        )
    elif structure is None:
        # Ideally get the 3-D geometry if available.
        pubchempy_molecule = _get_from_pubchem_with_retries(
            identifier=name, namespace='name', record_type='3d'
        )

        # If the 3-D geometry isn't available, get the 2-D geometry instead.
        if not pubchempy_molecule:
            pubchempy_molecule = _get_from_pubchem_with_retries(
                identifier=name, namespace='name', record_type='2d'
            )
    else:
        raise ValueError('Incorrect value for the argument structure=%s' % structure)

    # Check if pubchempy_molecule is an empty list or None
    if not pubchempy_molecule:
        print(
            "Unable to find structure info in the PubChem database"
            "for the specified molecule %s." % name
        )
        return None

    pubchempy_geometry = pubchempy_molecule[0].to_dict(properties=['atoms'])['atoms']
    geometry = [
        (atom['element'], (atom['x'], atom['y'], atom.get('z', 0))) for atom in pubchempy_geometry
    ]

    return geometry
